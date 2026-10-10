
from pathlib import Path

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas


GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


# Certificate color palette
NAVY = HexColor("#142B4A")
GOLD = HexColor("#B68A35")
LIGHT_GOLD = HexColor("#DCC58B")
IVORY = HexColor("#FFFCF4")
DARK_TEXT = HexColor("#26364A")


def draw_corner_decoration(pdf, x, y, direction_x, direction_y):
    """Draw decorative gold lines in each corner."""

    pdf.saveState()
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.2)

    # Horizontal and vertical decorative lines
    pdf.line(
        x, y,
        x + (25 * direction_x), y
    )

    pdf.line(
        x, y,
        x, y + (25 * direction_y)
    )

    pdf.setLineWidth(0.6)

    pdf.line(
        x + (5 * direction_x),
        y + (7 * direction_y),
        x + (17 * direction_x),
        y + (7 * direction_y)
    )

    pdf.line(
        x + (7 * direction_x),
        y + (5 * direction_y),
        x + (7 * direction_x),
        y + (17 * direction_y)
    )

    pdf.restoreState()


def draw_achievement_seal(pdf, x, y):
    """Draw a simple decorative achievement seal."""

    pdf.saveState()

    # Outer circles
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.8)
    pdf.circle(x, y, 29, stroke=1, fill=0)

    pdf.setStrokeColor(LIGHT_GOLD)
    pdf.setLineWidth(0.8)
    pdf.circle(x, y, 24, stroke=1, fill=0)

    # Inner circle
    pdf.setFillColor(NAVY)
    pdf.circle(x, y, 17, stroke=0, fill=1)

    # Star emblem
    pdf.setFillColor(GOLD)
    pdf.setFont("Times-Bold", 23)
    pdf.drawCentredString(x, y - 8, "*")

    # Small text below the seal
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.drawCentredString(x, y - 40, "ACHIEVEMENT")

    pdf.restoreState()


def generate_certificate(
    recipient_name: str,
    event_name: str,
    event_date: str,
    issuer: str,
    certificate_number: str
) -> str:

    # Output file
    file_name = f"{certificate_number}.pdf"
    file_path = GENERATED_DIR / file_name

    # Landscape A4 dimensions
    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=landscape(A4)
    )

    # --------------------------------------------------
    # 1. Background
    # --------------------------------------------------

    pdf.setFillColor(IVORY)
    pdf.rect(
        0, 0,
        page_width, page_height,
        stroke=0,
        fill=1
    )

    # --------------------------------------------------
    # 2. Double border
    # --------------------------------------------------

    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(2.2)

    pdf.rect(
        15, 15,
        page_width - 30,
        page_height - 30,
        stroke=1,
        fill=0
    )

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1)

    pdf.rect(
        23, 23,
        page_width - 46,
        page_height - 46,
        stroke=1,
        fill=0
    )

    # Inner decorative border
    pdf.setStrokeColor(LIGHT_GOLD)
    pdf.setLineWidth(0.5)

    pdf.rect(
        32, 32,
        page_width - 64,
        page_height - 64,
        stroke=1,
        fill=0
    )

    # --------------------------------------------------
    # 3. Decorative corners
    # --------------------------------------------------

    draw_corner_decoration(pdf, 38, 38, 1, 1)
    draw_corner_decoration(
        pdf, page_width - 38, 38, -1, 1
    )
    draw_corner_decoration(
        pdf, 38, page_height - 38, 1, -1
    )
    draw_corner_decoration(
        pdf,
        page_width - 38,
        page_height - 38,
        -1,
        -1
    )

    # --------------------------------------------------
    # 4. Main heading
    # --------------------------------------------------

    pdf.setFillColor(NAVY)
    pdf.setFont("Times-Bold", 35)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 91,
        "CERTIFICATE"
    )

    pdf.setFillColor(GOLD)
    pdf.setFont("Times-Bold", 18)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 119,
        "O F   C O M P L E T I O N"
    )

    # Decorative divider
    divider_y = page_height - 135
    center_x = page_width / 2

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(0.9)

    pdf.line(
        center_x - 125, divider_y,
        center_x - 10, divider_y
    )

    pdf.line(
        center_x + 10, divider_y,
        center_x + 125, divider_y
    )

    # Center diamond
    path = pdf.beginPath()
    path.moveTo(center_x, divider_y + 4)
    path.lineTo(center_x + 4, divider_y)
    path.lineTo(center_x, divider_y - 4)
    path.lineTo(center_x - 4, divider_y)
    path.close()

    pdf.setFillColor(GOLD)
    pdf.drawPath(path, stroke=0, fill=1)

    # Achievement seal in the upper-right area
    draw_achievement_seal(
        pdf,
        page_width - 105,
        page_height - 105
    )

    # --------------------------------------------------
    # 5. Award description
    # --------------------------------------------------

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Times-Roman", 15)

    pdf.drawCentredString(
        center_x,
        page_height - 183,
        "This certificate is proudly awarded to"
    )

    # --------------------------------------------------
    # 6. Recipient name
    # --------------------------------------------------

    pdf.setFillColor(NAVY)
    pdf.setFont("Times-Italic", 31)

    pdf.drawCentredString(
        center_x,
        page_height - 231,
        recipient_name
    )

    # Decorative line below recipient
    recipient_line_y = page_height - 245

    pdf.setStrokeColor(LIGHT_GOLD)
    pdf.setLineWidth(0.8)

    pdf.line(
        center_x - 100, recipient_line_y,
        center_x - 8, recipient_line_y
    )

    pdf.line(
        center_x + 8, recipient_line_y,
        center_x + 100, recipient_line_y
    )

    # --------------------------------------------------
    # 7. Event information
    # --------------------------------------------------

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Times-Roman", 14)

    pdf.drawCentredString(
        center_x,
        page_height - 275,
        "for successfully completing"
    )

    pdf.setFillColor(NAVY)
    pdf.setFont("Times-Bold", 23)

    pdf.drawCentredString(
        center_x,
        page_height - 309,
        event_name
    )

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Times-Roman", 13)

    pdf.drawCentredString(
        center_x,
        page_height - 343,
        f"Date: {event_date}"
    )

    
    # --------------------------------------------------
    # 7A. Appreciation message
    # --------------------------------------------------

    message_top = page_height - 385

    # Section heading
    pdf.setFillColor(GOLD)
    pdf.setFont("Times-Bold", 13)

    pdf.drawCentredString(
        center_x,
        message_top,
        "RECOGNITION & APPRECIATION"
    )

    # Decorative divider
    divider_y = message_top - 12

    pdf.setStrokeColor(LIGHT_GOLD)
    pdf.setLineWidth(0.8)

    pdf.line(
        center_x - 75,
        divider_y,
        center_x + 75,
        divider_y
    )

    # Universal appreciation message
    appreciation_lines = [
        "Your dedication, enthusiasm, and commitment are truly",
        "appreciated. Your participation and contribution reflect",
        "a willingness to learn, grow, and embrace new challenges.",
        "We commend your efforts and wish you continued success",
        "in your future endeavors."
    ]

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Times-Roman", 11.5)

    text_y = divider_y - 23

    for line in appreciation_lines:
        pdf.drawCentredString(
            center_x,
            text_y,
            line
        )
        text_y -= 17


    # --------------------------------------------------
    # 8. Issuer section - bottom left
    # --------------------------------------------------

    issuer_x = 155

    pdf.setFillColor(NAVY)
    pdf.setFont("Times-Bold", 17)

    pdf.drawCentredString(
        issuer_x,
        77,
        issuer
    )

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(0.8)

    pdf.line(
        issuer_x - 82, 68,
        issuer_x + 82, 68
    )

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica", 9)

    pdf.drawCentredString(
        issuer_x,
        51,
        f"Certificate ID: {certificate_number}"
    )

    # --------------------------------------------------
    # 9. Authorized signature - bottom right
    # --------------------------------------------------

    signature_x_start = page_width - 265
    signature_x_end = page_width - 85
    signature_y = 75

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1)

    pdf.line(
        signature_x_start,
        signature_y,
        signature_x_end,
        signature_y
    )

    pdf.setFillColor(DARK_TEXT)
    pdf.setFont("Helvetica", 9)

    pdf.drawCentredString(
        (signature_x_start + signature_x_end) / 2,
        signature_y - 16,
        "Authorized Signature"
    )

    # --------------------------------------------------
    # 10. Save the PDF
    # --------------------------------------------------

    pdf.save()

    return str(file_path)
