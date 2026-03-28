from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import time

def generate_invoice(text, items=None, shop_info=None, default_gst=18):
    name = f"invoice_{int(time.time())}.pdf"
    doc = SimpleDocTemplate(name, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("INVOICE", styles['Title']))
    content.append(Spacer(1, 0.25 * inch))

    # Parse text
    data = {}
    for line in text.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            data[key.strip().lower().replace(' ', '_')] = value.strip()

    # Shop Info
    if shop_info:
        shop_lines = []
        if shop_info.get('name'): shop_lines.append(f"<b>{shop_info['name']}</b>")
        if shop_info.get('address'): shop_lines.append(shop_info['address'])
        if shop_info.get('phone'): shop_lines.append(f"Phone: {shop_info['phone']}")
        if shop_info.get('email'): shop_lines.append(f"Email: {shop_info['email']}")
        company_str = "<br/>".join(shop_lines)
    else:
        company_str = "<b>Company Name</b><br/>Address<br/>Phone: 0000000000"

    content.append(Paragraph(company_str, styles['Normal']))
    content.append(Spacer(1, 0.2 * inch))

    # Invoice Info
    inv_no = data.get('invoice_number', f"INV-{int(time.time())}")
    inv_date = data.get('date', time.strftime("%Y-%m-%d"))
    customer = data.get('customer', 'Customer')

    content.append(Paragraph(f"Invoice #: {inv_no}<br/>Date: {inv_date}", styles['Normal']))
    content.append(Spacer(1, 0.15 * inch))
    content.append(Paragraph(f"<b>Bill To:</b> {customer}", styles['Normal']))
    content.append(Spacer(1, 0.3 * inch))

    # TABLE DATA
    table_data = []

    # Header
    table_data.append([
        'Description', 'Category', 'Qty', 'Unit Price', 'GST %', 'GST Amt', 'Total'
    ])

    subtotal = 0
    total_gst = 0

    # Items
    if items:
        for item in items:
            desc = item.get('product', '')
            category = item.get('category', 'General')
            qty = item.get('quantity', 1)
            price = item.get('unit_price', 0)
            gst_rate = item.get('gst_rate', default_gst)

            base_total = qty * price
            gst_amount = (base_total * gst_rate) / 100
            total = base_total + gst_amount

            subtotal += base_total
            total_gst += gst_amount

            table_data.append([
                desc,
                category,
                str(qty),
                f"{price:.2f}",
                f"{gst_rate}%",
                f"{gst_amount:.2f}",
                f"{total:.2f}"
            ])
    else:
        table_data.append(['No items', '', '', '', '', '', ''])

    # Add spacing row before totals
    table_data.append(['', '', '', '', '', '', ''])

    # Totals INSIDE SAME TABLE
    grand_total = subtotal + total_gst

    table_data.append(['', '', '', '', 'Subtotal', '', f"{subtotal:.2f}"])
    table_data.append(['', '', '', '', 'Total GST', '', f"{total_gst:.2f}"])
    table_data.append(['', '', '', '', 'Grand Total', '', f"{grand_total:.2f}"])

    # Create Table
    table = Table(table_data, colWidths=[2*inch, 1.2*inch, 0.7*inch, 1*inch, 0.8*inch, 1*inch, 1*inch])

    # Styling
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        # Grid
        ('GRID', (0,0), (-1,-1), 0.75, colors.black),

        # Alignment
        ('ALIGN', (2,1), (-1,-1), 'CENTER'),
        ('ALIGN', (3,1), (-1,-1), 'RIGHT'),

        # Padding
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TOPPADDING', (0,0), (-1,0), 10),

        # Totals Styling
        ('FONTNAME', (-2,-3), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (-2,-1), (-1,-1), colors.lightgrey),

        # Remove borders for empty spacer row
        ('LINEBELOW', (0,-4), (-1,-4), 0, colors.white),
    ]))

    content.append(table)

    # Footer
    content.append(Spacer(1, 0.4 * inch))
    content.append(Paragraph("Thank you for your business!", styles['Italic']))

    doc.build(content)

    return name