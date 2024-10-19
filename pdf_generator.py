from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf(worksheet):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create the PDF content
    content = []
    
    # Add title
    content.append(Paragraph(worksheet.title, styles['Title']))
    content.append(Spacer(1, 12))
    
    # Add metadata
    content.append(Paragraph(f"Subject: {worksheet.subject}", styles['Normal']))
    content.append(Paragraph(f"Grade Level: {worksheet.grade_level}", styles['Normal']))
    content.append(Paragraph(f"Topic: {worksheet.topic}", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Add worksheet content
    content.append(Paragraph(worksheet.content, styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    buffer.seek(0)
    return buffer
