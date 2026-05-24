"""
Certificate Generation Module
Generates PDF certificates and QR codes for land verification
"""

import os
import qrcode
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from typing import Dict, Any
import hashlib

class PDFGenerator:
    """Generate professional PDF certificates"""
    
    def __init__(self, output_dir: str = 'certificates'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_certificate(self, cert_data: Dict[str, Any]) -> str:
        """Generate a PDF certificate for land verification"""
        
        cert_id = cert_data.get('certificate_id', 'CERT-UNKNOWN')
        pdf_path = os.path.join(self.output_dir, f"{cert_id}.pdf")
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.green,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.darkgreen,
            spaceAfter=12
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6
        )
        
        # Build story
        story = []
        
        # Title
        story.append(Paragraph("LAND VERIFICATION CERTIFICATE", title_style))
        story.append(Spacer(1, 12))
        
        # Certificate ID
        story.append(Paragraph(f"Certificate ID: <b>{cert_id}</b>", normal_style))
        story.append(Paragraph(f"Date of Issue: {datetime.now().strftime('%B %d, %Y')}", normal_style))
        story.append(Spacer(1, 20))
        
        # Farmer Details
        story.append(Paragraph("FARMER DETAILS", heading_style))
        story.append(Paragraph(f"Name: {cert_data.get('farmer_name', 'N/A')}", normal_style))
        story.append(Paragraph(f"Aadhar Number: {cert_data.get('aadhar', 'N/A')}", normal_style))
        story.append(Spacer(1, 10))
        
        # Land Details
        story.append(Paragraph("LAND DETAILS", heading_style))
        story.append(Paragraph(f"Land ID: {cert_data.get('land_id', 'N/A')}", normal_style))
        story.append(Paragraph(f"Grid Position: {cert_data.get('grid_position', 'N/A')}", normal_style))
        story.append(Paragraph(f"Area: {cert_data.get('area_acres', 'N/A')} acres", normal_style))
        story.append(Paragraph(f"Crop Type: {cert_data.get('crop_type', 'N/A')}", normal_style))
        story.append(Spacer(1, 10))
        
        # Verification Details
        story.append(Paragraph("VERIFICATION DETAILS", heading_style))
        story.append(Paragraph(f"Captured Location: {cert_data.get('captured_lat', 'N/A')}, {cert_data.get('captured_lng', 'N/A')}", normal_style))
        story.append(Paragraph(f"Distance from Center: {cert_data.get('distance', 'N/A')} meters", normal_style))
        story.append(Paragraph(f"Confidence Score: {cert_data.get('confidence', 'N/A')}%", normal_style))
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("This certificate is system-generated and validates the land ownership.", normal_style))
        story.append(Paragraph("For verification, scan the QR code or visit the official portal.", normal_style))
        story.append(Spacer(1, 30))
        
        # Signature line
        story.append(Paragraph("_________________________", normal_style))
        story.append(Paragraph("Authorized Signatory", normal_style))
        story.append(Paragraph("Land Verification Authority, Mandya", normal_style))
        
        # Build PDF
        doc.build(story)
        
        return pdf_path
    
    def create_advanced_certificate(self, cert_data: Dict[str, Any]) -> str:
        """Create an advanced certificate with more details"""
        return self.create_certificate(cert_data)


class QRCodeGenerator:
    """Generate QR codes for certificates"""
    
    def __init__(self, output_dir: str = 'certificates'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_qr(self, certificate_id: str, cert_data: Dict[str, Any]) -> str:
        """Generate QR code for certificate"""
        
        # Create QR data
        qr_data = {
            'certificate_id': certificate_id,
            'farmer_name': cert_data.get('farmer_name', ''),
            'land_id': cert_data.get('land_id', ''),
            'verification_date': datetime.now().isoformat(),
            'verification_url': f"/verify/{certificate_id}"
        }
        
        # Convert to string
        qr_string = f"Certificate: {certificate_id}\nFarmer: {cert_data.get('farmer_name', '')}\nLand: {cert_data.get('land_id', '')}\nDate: {datetime.now().strftime('%Y-%m-%d')}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_string)
        qr.make(fit=True)
        
        # Create image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_path = os.path.join(self.output_dir, f"{certificate_id}_qr.png")
        qr_img.save(qr_path)
        
        return qr_path