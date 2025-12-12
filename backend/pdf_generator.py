# backend/pdf_generator.py
# Simple, robust PDF report for InsightLoop.AI using fpdf2

from fpdf import FPDF
from datetime import datetime
import re


def render_markdown_table(pdf, table_md: str):
    """
    Render a Markdown table as a proper PDF table.
    """
    lines = table_md.strip().split('\n')
    if len(lines) < 3:
        return  # Not a valid table

    # Remove header separator
    table_lines = [line for line in lines if not line.startswith('|') or '---' not in line]

    # Parse rows
    rows = []
    for line in table_lines:
        if '|' in line:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            rows.append(cells)

    if not rows:
        return

    # Calculate column widths
    num_cols = len(rows[0])
    col_widths = [pdf.w / num_cols] * num_cols  # Equal widths

    # Draw table
    pdf.set_font("Times", "B", 7)  # Header bold
    for i, cell in enumerate(rows[0]):
        short_cell = cell[:15] + "..." if len(cell) > 15 else cell
        pdf.cell(col_widths[i], 6, safe_text(short_cell), border=1, align='C')
    pdf.ln()

    pdf.set_font("Times", "", 6)  # Body normal
    for row in rows[1:]:
        for i, cell in enumerate(row):
            short_cell = cell[:15] + "..." if len(cell) > 15 else cell
            pdf.cell(col_widths[i], 5, safe_text(short_cell), border=1)
        pdf.ln()


def safe_text(text: str) -> str:
    """
    Make text safe for core PDF fonts (latin-1):
    - Replace fancy quotes/dashes with simple ones
    - Shorten very long unbroken strings (URLs, tokens)
    - Drop any remaining unsupported characters
    """
    if not text:
        return ""

    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "-",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    def shorten_long_word(match: re.Match) -> str:
        chunk = match.group(0)
        return chunk[:60] + "..."

    text = re.sub(r"\S{80,}", shorten_long_word, text)

    return text.encode("latin-1", "ignore").decode("latin-1")


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 14)
        self.cell(0, 10, "InsightLoop.AI - Web Research Report", ln=True, align="C")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def generate_pdf(query: str, links: list[str], insights: str, extracted: list[dict], comparison_table: str = "") -> bytes:
    """
    Create a PDF report (query + insights + sources) and return it as bytes.
    """
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title Page
    pdf.set_font("Times", "B", 20)
    pdf.cell(0, 15, "InsightLoop.AI Research Report", ln=True, align="C")
    pdf.ln(2)
    pdf.set_font("Times", "", 14)
    pdf.multi_cell(0, 8, safe_text(f"Query: {query}"), align="C")
    pdf.ln(2)
    pdf.set_font("Times", "I", 12)
    pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
    pdf.ln(2)

    # Table of Contents (simple)
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 8, "Table of Contents", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 6, "1. Introduction", ln=True)
    pdf.cell(0, 6, "2. Key Insights", ln=True)
    if comparison_table:
        pdf.cell(0, 6, "3. Comparison Table", ln=True)
    pdf.cell(0, 6, "4. Sources", ln=True)
    pdf.cell(0, 6, "5. Methodology", ln=True)
    pdf.ln(2)

    # 1. Introduction
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 10, "1. Introduction", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 8, safe_text(f"This report presents the findings from an autonomous web research conducted by InsightLoop.AI based on the query: '{query}'. The agent crawled relevant web pages, extracted key information, and summarized the insights using advanced AI."))
    pdf.ln(2)

    # 2. Key Insights
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "2. Key Insights", ln=True)
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, safe_text(insights))
    pdf.ln(2)

    # 3. Comparison Table
    if comparison_table:
        pdf.set_font("Times", "B", 14)
        pdf.cell(0, 10, "3. Comparison Table", ln=True)
        pdf.ln(2)
        render_markdown_table(pdf, comparison_table)
        pdf.ln(2)

    # 4. Sources
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "4. Sources Used", ln=True)
    pdf.set_font("Times", "", 10)
    if not links:
        pdf.multi_cell(0, 5, "No sources available.")
    else:
        for i, url in enumerate(links, start=1):
            pdf.multi_cell(0, 5, safe_text(f"{i}. {url}"))
            pdf.ln(1)
    pdf.ln(2)

    # 5. Methodology
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "5. Methodology", ln=True)
    pdf.set_font("Times", "", 10)
    pdf.multi_cell(
        0,
        5,
        "Web pages were crawled using requests with user-agent headers. Text was extracted using BeautifulSoup, cleaned, and summarized using the InsightLoop AI agent. Extracted snippets were processed to generate insights and comparisons. Full raw data is available in the application UI.",
    )

    pdf_bytes = pdf.output(dest="S")
    return pdf_bytes.encode('latin-1')
