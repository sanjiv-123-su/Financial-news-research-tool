from fpdf import FPDF

class FinancialReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(24, 95, 165)          # #185FA5 blue
        self.cell(0, 10, "Financial Equity Research Report", align="C")
        self.ln(4)
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def _safe_text(text: str) -> str:
    """Strip non-latin1 characters FPDF core fonts can't encode."""
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def generate_pdf_report(summary: str, chat_history: list) -> bytearray:
    pdf = FinancialReportPDF(orientation="P", unit="mm", format="A4")

    # ── Explicit, sane margins ──────────────────────────────────────────
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_page()

    # ── Available width (always positive now) ──────────────────────────
    W = pdf.w - pdf.l_margin - pdf.r_margin   # 210 - 20 - 20 = 170mm

    # ── Summary section ────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(W, 8, "Market Summary", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for line in (summary or "No summary generated.").split("\n"):
        clean = _safe_text(line.strip())
        if clean:
            pdf.multi_cell(W, 6, clean)   # ← explicit W, never 0
        else:
            pdf.ln(3)

    # ── Chat history section ───────────────────────────────────────────
    if chat_history:
        pdf.ln(6)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(W, 8, "Query Log", ln=True)
        pdf.ln(2)

        for i, entry in enumerate(chat_history, 1):
            # Question
            pdf.set_fill_color(230, 241, 251)   # light blue bg
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(24, 95, 165)
            q_text = _safe_text(f"Q{i}: {entry.get('question', '')}")
            pdf.multi_cell(W, 7, q_text, fill=True)
            pdf.ln(1)

            # Answer
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(60, 60, 60)
            a_text = _safe_text(entry.get("answer", ""))
            for line in a_text.split("\n"):
                clean = line.strip()
                if clean:
                    pdf.multi_cell(W, 6, clean)
                else:
                    pdf.ln(3)
            pdf.ln(4)

    return pdf.output()