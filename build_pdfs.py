"""Build print-ready copies of the current Crankshaft launch documents."""
from pathlib import Path
from html import escape
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

INK = colors.HexColor("#1B2A31")
SOFT = colors.HexColor("#3D515A")
AMBER = colors.HexColor("#E6AB00")
LINE = colors.HexColor("#DCE3DF")
PALE = colors.HexColor("#F9F3DE")

STYLES = {
    "title": ParagraphStyle("Title", fontName="Arial-Bold", fontSize=21, leading=25, textColor=INK, spaceAfter=11),
    "h2": ParagraphStyle("H2", fontName="Arial-Bold", fontSize=13.5, leading=16.5, textColor=INK, spaceBefore=12, spaceAfter=6, keepWithNext=True),
    "h3": ParagraphStyle("H3", fontName="Arial-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=11, spaceAfter=5),
    "body": ParagraphStyle("Body", fontName="Arial", fontSize=8.9, leading=12.6, textColor=SOFT, spaceAfter=6),
    "list": ParagraphStyle("List", fontName="Arial", fontSize=8.9, leading=12.6, textColor=SOFT, leftIndent=14, firstLineIndent=-10, spaceAfter=3),
    "cell": ParagraphStyle("Cell", fontName="Arial", fontSize=8.3, leading=11.2, textColor=SOFT, alignment=TA_LEFT),
    "head": ParagraphStyle("Head", fontName="Arial-Bold", fontSize=8.3, leading=11.2, textColor=INK),
}

LINK_RE = re.compile(r"\[([^]]+)\]\(([^)]+)\)")

def inline(value: str) -> str:
    out = []
    pos = 0
    for match in LINK_RE.finditer(value):
        out.append(escape(value[pos:match.start()]))
        label = escape(match.group(1))
        href = escape(match.group(2), quote=True)
        out.append(f'<link href="{href}" color="#8B5C00">{label}</link>')
        pos = match.end()
    out.append(escape(value[pos:]))
    txt = "".join(out)
    txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", txt)
    txt = re.sub(r"`([^`]+)`", r'<font name="Arial-Bold">\1</font>', txt)
    return txt

def table_from(lines):
    rows = []
    for line in lines:
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", x or "") for x in cells):
            continue
        rows.append(cells)
    if not rows:
        return None
    count = max(len(r) for r in rows)
    width = letter[0] - 1.3 * inch
    if count == 4:
        col_widths = [width * .43] + [width * .19] * 3
    elif count == 3:
        col_widths = [width * .44] + [width * .28] * 2
    else:
        col_widths = [width / count] * count
    data = []
    for i, row in enumerate(rows):
        row += [""] * (count - len(row))
        data.append([Paragraph(inline(x), STYLES["head"] if i == 0 else STYLES["cell"]) for x in row])
    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0,0),(-1,0), PALE),
        ("VALIGN", (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("TOPPADDING", (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LINEBELOW", (0,0),(-1,-1), .4, LINE),
    ]
    for i in range(2, len(data), 2):
        commands.append(("BACKGROUND", (0,i),(-1,i), colors.HexColor("#F7F9F7")))
    t.setStyle(TableStyle(commands))
    return t

def page_frame(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setFillColor(colors.HexColor("#23282A"))
    canvas.rect(0, h-43, w, 43, fill=1, stroke=0)
    canvas.setFillColor(AMBER)
    canvas.rect(0, h-46, w, 3, fill=1, stroke=0)
    canvas.setFont("Arial-Bold", 10)
    canvas.setFillColor(colors.white)
    canvas.drawString(.65*inch, h-28, "CRANKSHAFT  /  LAUNCH PACKAGE")
    canvas.setStrokeColor(LINE)
    canvas.line(.65*inch, .54*inch, w-.65*inch, .54*inch)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(SOFT)
    canvas.drawString(.65*inch, .36*inch, "Internal planning document  •  October 2026")
    canvas.drawRightString(w-.65*inch, .36*inch, str(doc.page))
    canvas.restoreState()

def render(md_path: Path, pdf_path: Path):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    styles = STYLES.copy()
    if md_path.name == "Business-Plan.md":
        styles["title"] = STYLES["title"].clone("BusinessPlanTitle", fontSize=20, leading=23, spaceAfter=8)
        styles["h2"] = STYLES["h2"].clone("BusinessPlanH2", fontSize=12.5, leading=15, spaceBefore=9, spaceAfter=4)
        styles["body"] = STYLES["body"].clone("BusinessPlanBody", fontSize=8.5, leading=11.4, spaceAfter=4)
        styles["list"] = STYLES["list"].clone("BusinessPlanList", fontSize=8.5, leading=11.4, spaceAfter=2)
    story = []
    i = 0
    while i < len(lines):
        raw = lines[i].strip()
        if not raw:
            i += 1
            continue
        if raw.startswith("|"):
            group = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                group.append(lines[i].strip())
                i += 1
            table = table_from(group)
            if table:
                story.extend([Spacer(1, 7), table, Spacer(1, 10)])
            continue
        if raw.startswith("# "):
            story.append(Paragraph(inline(raw[2:]), styles["title"]))
        elif raw.startswith("## "):
            story.append(Paragraph(inline(raw[3:]), styles["h2"]))
        elif raw.startswith("### "):
            story.append(Paragraph(inline(raw[4:]), styles["h3"]))
        elif re.match(r"^([-*]|\d+\.)\s+", raw):
            text = re.sub(r"^([-*]|\d+\.)\s+", "", raw)
            story.append(Paragraph("• " + inline(text), styles["list"]))
        else:
            paragraph = [raw]
            while i + 1 < len(lines) and lines[i+1].strip() and not re.match(r"^(#|\||[-*] |\d+\. )", lines[i+1].strip()):
                i += 1
                paragraph.append(lines[i].strip())
            story.append(Paragraph(inline(" ".join(paragraph)), styles["body"]))
        i += 1
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, leftMargin=.65*inch, rightMargin=.65*inch, topMargin=.76*inch, bottomMargin=.65*inch, title=lines[0].lstrip("# "), author="Crankshaft")
    doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
    print(pdf_path.relative_to(ROOT))

for source, target in [
    ("Business-Plan.md", "plan/Crankshaft-Business-Plan.pdf"),
    ("Business-Model.md", "plan/Crankshaft-Business-Model.pdf"),
    ("Investor-Brief.md", "plan/Crankshaft-Investor-Brief.pdf"),
    ("Dealer-Service-Guide.md", "sales/Crankshaft-Dealer-Service-Guide.pdf"),
]:
    render(ROOT/source, ROOT/target)
