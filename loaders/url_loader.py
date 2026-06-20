import re
from langchain_core.documents import Document

try:
    from curl_cffi import requests  # mimics Chrome TLS — bypasses bot detection
    CURL_AVAILABLE = True
except ImportError:
    import requests                 # fallback
    CURL_AVAILABLE = False

try:
    from newspaper import Article
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False

from bs4 import BeautifulSoup


class FinancialURLLoader:
    """
    Two-strategy extractor:
      1. curl_cffi  → mimics Chrome TLS, bypasses Cloudflare/bot detection
      2. newspaper3k → clean article extraction for standard news sites
    """

    MIN_LENGTH = 200

    def __init__(self, urls):
        self.urls = [url.strip() for url in urls if url.strip()]

    def load(self) -> list[Document]:
        documents = []
        failed = []

        for index, url in enumerate(self.urls):
            print(f"\n[{index+1}/{len(self.urls)}] Fetching: {url}")

            # Strategy 1: curl_cffi (best for bot-protected sites)
            text, title = self._extract_curl(url)

            # Strategy 2: newspaper3k fallback
            if not self._sufficient(text):
                print("  → curl_cffi thin, trying newspaper3k...")
                text, title = self._extract_newspaper(url)

            if not self._sufficient(text):
                print(f"  → SKIPPED (extracted only {len(text)} chars)")
                failed.append(url)
                continue

            documents.append(Document(
                page_content=self.clean_text(text),
                metadata={
                    "source": url,
                    "title": self.clean_text(title or f"Article {index+1}"),
                    "source_id": index + 1,
                }
            ))
            print(f"  → OK: {len(text)} chars | \"{(title or '')[:60]}\"")

        if not documents:
            tips = "\n".join(f"  • {u}" for u in failed)
            raise ValueError(
                f"Could not extract content from any URL.\n\n"
                f"Failed URLs:\n{tips}\n\n"
                f"Likely causes:\n"
                f"  • Hard paywalls (Bloomberg, WSJ, FT)\n"
                f"  • Cloudflare / bot protection\n"
                f"  • JS-only rendering (try adding Selenium)\n\n"
                f"Recommended free sources:\n"
                f"  • https://economictimes.indiatimes.com/\n"
                f"  • https://www.moneycontrol.com/\n"
                f"  • https://www.livemint.com/\n"
                f"  • https://www.ndtvprofit.com/"
            )

        return documents

    def _extract_curl(self, url: str) -> tuple[str, str]:
        """Chrome TLS impersonation via curl_cffi."""
        if not CURL_AVAILABLE:
            return "", ""
        try:
            r = requests.get(url, impersonate="chrome120", timeout=15)
            print(f"  → curl_cffi status: {r.status_code} | {len(r.content)} bytes")
            if r.status_code != 200:
                return "", ""

            soup = BeautifulSoup(r.content, "html.parser")
            for tag in soup(["script", "style", "header", "footer", "nav",
                              "aside", "form", "button", "iframe"]):
                tag.decompose()

            # Try <p> tags first
            text = " ".join(p.get_text() for p in soup.find_all("p"))

            # Fallback to semantic containers
            if not self._sufficient(text):
                for sel in ["article", "main", "[class*='article-body']",
                             "[class*='story-body']", "[class*='content']"]:
                    el = soup.select_one(sel)
                    if el:
                        text = el.get_text(separator=" ", strip=True)
                        if self._sufficient(text):
                            break

            title = soup.title.string if soup.title else ""
            return text, title

        except Exception as e:
            print(f"  → curl_cffi error: {e}")
            return "", ""

    def _extract_newspaper(self, url: str) -> tuple[str, str]:
        """newspaper3k — good for standard news article URLs."""
        if not NEWSPAPER_AVAILABLE:
            return "", ""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text, article.title
        except Exception as e:
            print(f"  → newspaper3k error: {e}")
            return "", ""

    def _sufficient(self, text: str) -> bool:
        return bool(text) and len(text.strip()) >= self.MIN_LENGTH

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', ' ', text)
        return text.strip()