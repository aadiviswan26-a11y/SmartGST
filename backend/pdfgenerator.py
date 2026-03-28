from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import time

# CATEGORY ENGINE
from backend.category_rules import auto_detect_slab, RATE_TO_CATEGORY_NAME


def generate_invoice(text, items=None, shop_info=None, default_gst=18):
    name = f"invoice_{int(time.time())}.pdf"

    # PAGE SETUP
    doc = SimpleDocTemplate(
        name,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # ✅ DEFAULT FONT (NO CUSTOM FONT)
    normal_style = ParagraphStyle(
        'Clean',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        spaceAfter=2
    )

    bold_style = ParagraphStyle(
        'Bold',
        parent=normal_style,
        fontName='Helvetica-Bold'
    )

    title_style = ParagraphStyle(
        'TitleFix',
        parent=styles['Title'],
        fontName='Helvetica-Bold'
    )

    content = []

    # -------- TITLE --------
    content.append(Paragraph("INVOICE", title_style))
    content.append(Spacer(1, 0.25 * inch))

    # -------- PARSE INPUT --------
    data = {}
    for line in text.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            data[key.strip().lower().replace(' ', '_')] = value.strip()

    # -------- SHOP INFO --------
    if shop_info:
        shop_lines = []
        if shop_info.get('name'):
            shop_lines.append(f"<b>{shop_info['name']}</b>")
        if shop_info.get('address'):
            shop_lines.append(shop_info['address'])
        if shop_info.get('phone'):
            shop_lines.append(f"Phone: {shop_info['phone']}")
        if shop_info.get('email'):
            shop_lines.append(f"Email: {shop_info['email']}")

        company_str = "<br/>".join(shop_lines)
    else:
        company_str = "<b>Company Name</b><br/>Address<br/>Phone: 0000000000"

    content.append(Paragraph(company_str, normal_style))
    content.append(Spacer(1, 0.2 * inch))

    # -------- INVOICE INFO --------
    inv_no = data.get('invoice_number', f"INV-{int(time.time())}")
    inv_date = data.get('date', time.strftime("%Y-%m-%d"))
    customer = data.get('customer', 'Customer')

    content.append(Paragraph(f"Invoice #: {inv_no}<br/>Date: {inv_date}", normal_style))
    content.append(Spacer(1, 0.15 * inch))
    content.append(Paragraph(f"<b>Bill To:</b> {customer}", normal_style))
    content.append(Spacer(1, 0.3 * inch))

    # -------- TABLE --------
    table_data = []
    headers = ["Description", "Category", "Qty", "Unit Price", "GST %", "GST Amt", "Total"]
    table_data.append([Paragraph(f"<b>{h}</b>", normal_style) for h in headers])

    subtotal = 0
    total_gst = 0

    # -------- ITEMS --------
    if items:
        for item in items:
            desc = str(item.get('product', '')).strip()
            qty = item.get('quantity', 1)
            price = item.get('unit_price', 0)

            # GST AUTO DETECT (FIXED FALLBACK)
            gst_rate = item.get('gst_rate')
            if gst_rate is None or gst_rate == 0:
                gst_rate = auto_detect_slab(desc.lower()) or default_gst

            category = item.get('category') or RATE_TO_CATEGORY_NAME.get(gst_rate, "General")

            base_total = qty * price
            gst_amount = (base_total * gst_rate) / 100
            total = base_total + gst_amount

            subtotal += base_total
            total_gst += gst_amount

            table_data.append([
                Paragraph(desc or " ", normal_style),
                Paragraph(category or " ", normal_style),
                Paragraph(str(qty), normal_style),
                Paragraph(f"Rs. {price:,.2f}", normal_style),
                Paragraph(f"{gst_rate}%", normal_style),
                Paragraph(f"Rs. {gst_amount:,.2f}", normal_style),
                Paragraph(f"Rs. {total:,.2f}", normal_style),
            ])
    else:
        table_data.append([Paragraph("No items", normal_style)] * 7)

    grand_total = subtotal + total_gst

    # -------- TOTAL ROWS --------
    empty = Paragraph(" ", normal_style)

    table_data.append([empty]*4 + [
        Paragraph("Subtotal", bold_style), empty, Paragraph(f"Rs. {subtotal:,.2f}", bold_style)
    ])

    table_data.append([empty]*4 + [
        Paragraph("Total GST", bold_style), empty, Paragraph(f"Rs. {total_gst:,.2f}", bold_style)
    ])

    table_data.append([empty]*4 + [
        Paragraph("Grand Total", bold_style), empty, Paragraph(f"Rs. {grand_total:,.2f}", bold_style)
    ])

    # -------- TABLE DESIGN --------
    table = Table(table_data, colWidths=[
        2.0 * inch,
        1.5 * inch,
        0.6 * inch,
        0.9 * inch,
        0.7 * inch,
        0.9 * inch,
        1.0 * inch
    ])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1f3c88")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),

        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),

        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('BACKGROUND', (-1, -1), (-1, -1), colors.HexColor("#dfe6e9")),
    ]))

    content.append(table)

    # -------- FOOTER --------
    content.append(Spacer(1, 0.4 * inch))
    content.append(Paragraph("Thank you for your business!", normal_style))

    doc.build(content)

    return name
