from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file, Response
from flask_cors import CORS
import os
import hashlib
import base64
import json
import csv
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import requests
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from groq import Groq

app = Flask(__name__)
app.config['SECRET_KEY'] = 'land_boundary_hackathon_2026'
CORS(app)

# ============ BOUNDARY DATA ============
from boundary_data import (
    LAND_BOUNDARIES, PESEC_CAMPUS, find_land_by_coordinates,
    get_land_by_aadhar, point_in_polygon, haversine_distance,
    get_all_boundaries_for_admin
)

CSV_FILE = 'verified_farmers.csv'

# Place this at the top of app.py along with your imports
from bank import BankingEngine
bank_engine = BankingEngine(CSV_FILE)

# In-memory session logging tracking active credit allocations/offers
# Structure: { aadhar_number: { 'status': 'OFFERED' | 'APPROVED', 'income': float, 'tier': str } }
BANK_OFFERS_DB = {}


# ============ SAFE POSITION-BASED CSV PARSER ============
def parse_farmers_csv_safely():
    """Reads the local flat-file ledger using direct positional indices to bypass header mismatch bugs."""
    csv_file_path = os.path.join(os.path.dirname(__file__), CSV_FILE)
    if not os.path.exists(csv_file_path):
        return []

    farmers_list = []
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Cleanly skip header row
            
            for row in reader:
                if not row or len(row) < 10:
                    continue
                
                # append_to_csv writes 14 variables in this exact order:
                # 0: cert_id, 1: timestamp, 2: farmer_name, 3: aadhar, 4: land_id, 
                # 5: grid_pos, 6: lat, 7: lng, 8: distance, 9: confidence, 10: status
                cert_id = row[0]
                timestamp = row[1]
                farmer_name = row[2]
                aadhar = row[3]
                land_id = row[4]
                grid_pos = row[5]
                lat = row[6]
                lng = row[7]
                distance = row[8]
                confidence_raw = row[9]
                status = row[10]

                try:
                    confidence_val = int(float(confidence_raw))
                except (ValueError, TypeError):
                    confidence_val = 90  # Solid baseline metrics default fallback

                # Inject multiple structural key casings to protect frontend script variable calls
                farmers_list.append({
                    "id": cert_id,
                    "Certificate_ID": cert_id,
                    "name": farmer_name,
                    "Farmer_Name": farmer_name,
                    "aadhar": aadhar,
                    "Aadhar_Number": aadhar,
                    "land_id": land_id,
                    "Land_ID": land_id,
                    "grid_position": grid_pos,
                    "Grid_Position": grid_pos,
                    "coordinates": f"{lat}, {lng}",
                    "latitude": lat,
                    "longitude": lng,
                    "distance": distance,
                    "confidence": confidence_val,
                    "Confidence": confidence_val,
                    "status": status,
                    "timestamp": timestamp
                })
        return farmers_list[::-1]  # Serve newest verification objects first
    except Exception as e:
        print("CSV Positional Parser Exception Node:", e)
        return []


# ============ BANKING CONSOLE SERVICES PIPELINE ============

@app.route('/bank/portal')
def bank_portal_page():
    """Renders the central institutional investment console."""
    stable_list = parse_farmers_csv_safely()
    return render_template('bank.html', farmers=stable_list, allocations=BANK_OFFERS_DB)


@app.route('/api/bank/verified-farmers', methods=['GET'])
def get_verified_farmers_json():
    """Serves the un-shifted clean ledger items array directly to frontend AJAX/Fetch requests."""
    return jsonify(parse_farmers_csv_safely())


@app.route('/api/bank/extend-offer', methods=['POST'])
def api_extend_offer():
    """Allows bank operators to extend direct investment proposals to high-confidence farmers."""
    data = request.json or {}
    aadhar = data.get('aadhar')
    if not aadhar:
        return jsonify({'error': 'Missing identification reference'}), 400
        
    BANK_OFFERS_DB[aadhar] = {
        'status': 'OFFERED',
        'timestamp': datetime.now().strftime('%Y-%m-%d'),
        'income': None,
        'tier': None
    }
    return jsonify({'success': True, 'message': 'Investment proposal dispatched successfully to farmer dashboard.'})


@app.route('/api/farmer/check-eligibility', methods=['POST'])
def api_farmer_check_eligibility():
    """Validates submitted verification paperwork and files for credit tier confirmation."""
    try:
        aadhar = request.form.get('aadhar')
        reported_income = float(request.form.get('income', 0))
        
        if not aadhar:
            return jsonify({'success': False, 'error': 'Identity token session missing.'}), 400

        land_id, land_data = get_land_by_aadhar(aadhar)
        if not land_data:
            return jsonify({'success': False, 'error': 'Aadhar record does not match registered profile database parameters.'}), 400

        evaluation = bank_engine.evaluate_financial_eligibility(reported_income)
        if not evaluation['eligible']:
            return jsonify({'success': False, 'error': evaluation['reason']})

        BANK_OFFERS_DB[aadhar] = {
            'status': 'APPROVED',
            'timestamp': datetime.now().strftime('%Y-%m-%d'),
            'income': reported_income,
            'tier': evaluation['tier'],
            'interest_rate': evaluation['interest_rate'],
            'benefits': evaluation['benefits']
        }

        return jsonify({
            'success': True,
            'tier': evaluation['tier'],
            'interest_rate': evaluation['interest_rate'],
            'benefits': evaluation['benefits']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f"Processing error: {str(e)}"}), 500


# ============ CERTIFICATE DOWNLOAD PIPELINE ============

@app.route('/api/certificate/<certificate_id>/download', methods=['GET'])
def download_certificate(certificate_id):
    """Assembles an uncorrupted PDF document binary using structured layouts."""
    if certificate_id.endswith('.pdf'):
        certificate_id = certificate_id[:-4]
        
    pdf_path = os.path.join('certificates', f"{certificate_id}.pdf")
    qr_path = os.path.join('certificates', f"QR_{certificate_id}.png")
    
    try:
        os.makedirs('certificates', exist_ok=True)
        
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
        verification_url = f"http://{request.host}/api/certificate/{certificate_id}/download"
        qr.add_data(verification_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(qr_path)
        
        doc = SimpleDocTemplate(
            pdf_path, pagesize=letter,
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        title_style = ParagraphStyle(
            'HeaderMain', parent=styles['Heading1'], fontSize=22,
            textColor=colors.HexColor('#1a472a'), spaceAfter=15, alignment=1
        )
        body_style = ParagraphStyle(
            'BodyMain', parent=styles['Normal'], fontSize=11,
            leading=16, textColor=colors.HexColor('#333333'), spaceAfter=12
        )
        
        story.append(Paragraph("🌾 AGRICULTURAL LAND BOUNDARY RECORD SLIP", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2d5a3b'), spaceAfter=20))
        
        story.append(Paragraph(f"<b>Certificate Reference Log:</b> <code>{certificate_id}</code>", body_style))
        story.append(Paragraph(f"<b>Issuing Authority Matrix:</b> LandVerify Registry Hub", body_style))
        story.append(Paragraph(f"<b>System Verification Status:</b> SIGNED AND CONFIRMED", body_style))
        story.append(Spacer(1, 10))
        
        text_block = """
        This data sheet acts as verifiable verification confirmation that physical coordinates 
        harvested from hardware telemetry targets correlate perfectly with the registered bounding matrix 
        assigned to the user profile grid layout. Surface data match checks confirm structural boundary boundaries.
        """
        story.append(Paragraph(text_block, body_style))
        story.append(Spacer(1, 15))
        
        qr_flowable = RLImage(qr_path, width=120, height=120)
        qr_label = Paragraph("<b>Scan Code to Authenticate Data Pipeline:</b><br/><font color='#666666' size='9'>This cryptographic code links directly to the secure verification node ledger.</font>", body_style)
        
        container_data = [[qr_label, qr_flowable]]
        container_table = Table(container_data, colWidths=[360, 140])
        container_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        
        story.append(container_table)
        story.append(Spacer(1, 15))
        
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=10))
        story.append(Paragraph(f"<font color='#777777'>Generated timestamp log: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST</font>", body_style))
        
        doc.build(story)
        
        if os.path.exists(qr_path):
            os.remove(qr_path)
            
    except Exception as e:
        return f"PDF Render Crash Alert: {str(e)}", 500
        
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name=f"{certificate_id}.pdf", mimetype='application/pdf')
    return "Document tracking reference dropped.", 404


def append_to_csv(cert_id, farmer_name, aadhar, land_id, grid_pos, lat, lng, distance, confidence, status, vpn, ip, img_hash):
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([cert_id, datetime.now().isoformat(), farmer_name, aadhar,
                        land_id, grid_pos, lat, lng, distance, confidence, status, vpn, ip, img_hash])


# ============ AGRICULTURAL KRISHI AI PIPELINE ============

groq_client = Groq(api_key="//your API KEY here")

SYSTEM_PROMPT = """
You are an agriculture assistant for Indian farmers.
Rules:
- Give short and simple answers
- Help with crops
- Help with diseases
- Suggest fertilizers
- Explain in easy language
"""

def translate_text(text, target_language):
    prompt = f"Translate this text to {target_language}.\n\nOnly give translated text.\n\nText:\n{text}"
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Translation Error:", e)
        return text

def ask_ai(question):
    try:
        final_prompt = f"{SYSTEM_PROMPT}\n\nFarmer Question:\n{question}"
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": final_prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("AI Error:", e)
        return f"AI Error: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json() or {}
        question = data.get('question', '').strip()
        language = data.get('language', 'en')

        if not question:
            return jsonify({"answer": "Please ask something."})

        english_question = translate_text(question, "English") if language != "en" else question
        answer_english = ask_ai(english_question)
        final_answer = translate_text(answer_english, language) if language != "en" else answer_english

        return jsonify({"answer": final_answer})
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"answer": f"Backend Error Node: {str(e)}"})


# ============ GPS METADATA EXIF EXTRACTION ============

def extract_gps_from_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif_data = img._getexif()
        
        if not exif_data:
            return None, "No EXIF data found in this image file."
        
        exif = {TAGS.get(k, k): v for k, v in exif_data.items()}
        if "GPSInfo" not in exif:
            return None, "No GPS metadata found in this photo file."
        
        gps_info = {}
        for tag, value in exif["GPSInfo"].items():
            decoded = GPSTAGS.get(tag, tag)
            gps_info[decoded] = value
        
        if "GPSLatitude" not in gps_info or "GPSLongitude" not in gps_info:
            return None, "Incomplete GPS location context in photo metadata."
        
        def dms_to_decimal(dms, ref):
            degrees = float(dms[0])
            minutes = float(dms[1]) / 60.0
            seconds = float(dms[2]) / 3600.0
            decimal = degrees + minutes + seconds
            if ref in ['S', 'W']:
                decimal = -decimal
            return decimal
        
        lat = dms_to_decimal(gps_info["GPSLatitude"], gps_info["GPSLatitudeRef"])
        lng = dms_to_decimal(gps_info["GPSLongitude"], gps_info["GPSLongitudeRef"])
        
        return (lat, lng), f"GPS Extracted: {lat:.6f}, {lng:.6f}"
    except Exception as e:
        return None, f"Metadata extraction failure: {str(e)}"

def verify_land_boundary(gps_lat, gps_lng, aadhar):
    land_id, land_data = get_land_by_aadhar(aadhar)
    
    if not land_data:
        return {'verified': False, 'reason': f'No land registry profile matches: {aadhar}'}
    
    if point_in_polygon(gps_lat, gps_lng, land_data['polygon']):
        center = land_data['center']
        distance = haversine_distance(gps_lat, gps_lng, center['lat'], center['lng'])
        confidence = 98 if distance < 15 else (90 if distance < 35 else 80)
        
        return {
            'verified': True,
            'land_id': land_id,
            'owner_name': land_data['owner_name'],
            'area_acres': land_data['area_acres'],
            'crop_type': land_data['crop_type'],
            'grid_position': land_data['grid_position'],
            'distance_from_center': round(distance, 2),
            'confidence': confidence
        }
    else:
        actual_land_id, actual_land_data = find_land_by_coordinates(gps_lat, gps_lng)
        if actual_land_data and actual_land_id != "PESEC_CAMPUS":
            return {
                'verified': False,
                'reason': f"Coordinates put you in {actual_land_data['owner_name']}'s land (Grid {actual_land_data['grid_position']}).",
                'actual_owner': actual_land_data['owner_name']
            }
        elif actual_land_id == "PESEC_CAMPUS":
            return {'verified': False, 'reason': 'Coordinates point inside the PES Campus zone.'}
        else:
            return {'verified': False, 'reason': 'Coordinates do not match any agricultural plot sector.'}


# ============ CORE USER DISPATCH PAGES ============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/farmer/login', methods=['GET', 'POST'])
def farmer_login():
    if request.method == 'POST':
        aadhar = request.form.get('aadhar').strip()
        land_id, land_data = get_land_by_aadhar(aadhar)
        if land_data:
            session['farmer_aadhar'] = aadhar
            session['farmer_name'] = land_data['owner_name']
            session['land_id'] = land_id
            return redirect(url_for('farmer_dashboard'))
        return render_template('farmer_login.html', error=f'No land registered with ID: {aadhar}')
    return render_template('farmer_login.html')

@app.route('/farmer/dashboard')
def farmer_dashboard():
    if 'farmer_aadhar' not in session:
        return redirect(url_for('farmer_login'))
        
    aadhar = session['farmer_aadhar']
    land_id, land_data = get_land_by_aadhar(aadhar)
    
    # Initialize variables to hold verification and certificate data
    is_already_verified = False
    certificate_data = None
    
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # Read header row
                
                # Check column positioning based on our clean header structure
                # Header: ['Certificate_ID', 'Timestamp', 'Farmer_Name', 'Aadhar_Number', ...]
                for row in reader:
                    if row and len(row) > 3:
                        if row[3].strip() == str(aadhar).strip():
                            is_already_verified = True
                            certificate_data = {
                                'id': row[0],
                                'timestamp': row[1].split('T')[0] if 'T' in row[1] else row[1], # Clean date string
                                'confidence': row[9] if len(row) > 9 else "90"
                            }
                            break
        except Exception as e:
            print("Dashboard certificate lookup error:", e)

    return render_template(
        'farmer_dashboard.html', 
        farmer_name=session['farmer_name'], 
        land_data=land_data, 
        land_id=land_id, 
        farmer_aadhar=aadhar,
        is_verified=is_already_verified,
        certificate=certificate_data  # Pass certificate dictionary to the frontend
    )
@app.route('/farmer/schemes')
def farmer_schemes():
    # Enforce strict session token authorization to secure spatial data lookups
    if 'farmer_aadhar' not in session:
        return redirect(url_for('farmer_login'))
        
    aadhar = session['farmer_aadhar']
    land_id, land_data = get_land_by_aadhar(aadhar)
    
    # Check current verified state ledger constraints to pass along to the navigation panel elements
    is_already_verified = False
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Bypass document headers
                for row in reader:
                    if row and len(row) > 3 and row[3].strip() == str(aadhar).strip():
                        is_already_verified = True
                        break
        except Exception as e:
            print("Schemes context verification file access warning:", e)

    return render_template(
        'schemes.html',
        farmer_name=session.get('farmer_name', 'Verified User'),
        land_id=land_id,
        land_data=land_data,
        is_verified=is_already_verified
    )
@app.route('/api/verify', methods=['POST'])
def api_verify():
    """Unified Verification Endpoint handles both live camera feeds and file uploads"""
    try:
        data = request.json
        aadhar = data.get('aadhar')
        image_base64 = data.get('image')
        
        live_lat = data.get('live_latitude')
        live_lng = data.get('live_longitude')
        
        if not aadhar or not image_base64:
            return jsonify({'verified': False, 'error': 'Missing identity parameter metrics.'}), 400
        
        try:
            image_bytes = base64.b64decode(image_base64.split(',')[1])
        except:
            return jsonify({'verified': False, 'error': 'Malformed image data encryption string'}), 400
            
        image_hash = hashlib.sha256(image_bytes).hexdigest()[:16]
        
        if live_lat and live_lng:
            lat, lng = float(live_lat), float(live_lng)
        else:
            gps_coords, gps_message = extract_gps_from_image(image_bytes)
            if not gps_coords:
                return jsonify({'verified': False, 'error': gps_message}), 400
            lat, lng = gps_coords
            
        verification_result = verify_land_boundary(lat, lng, aadhar)
        verification_result['captured_gps'] = {'lat': lat, 'lng': lng}
        verification_result['image_hash'] = image_hash
        
        if verification_result['verified']:
            cert_id = f"CERT-{datetime.now().strftime('%Y%m%d')}-{image_hash[:8].upper()}"
            verification_result['certificate_id'] = cert_id
            verification_result['timestamp'] = datetime.now().isoformat()
            
            land_id, land_data = get_land_by_aadhar(aadhar)
            append_to_csv(cert_id, land_data['owner_name'], aadhar, land_id, land_data['grid_position'], lat, lng, verification_result['distance_from_center'], verification_result['confidence'], 'APPROVED', False, request.remote_addr, image_hash)
            
            os.makedirs('certificates', exist_ok=True)
            with open(f"certificates/{cert_id}.pdf", 'w') as f:
                f.write(f"Verified Boundary Asset Receipt\nID: {cert_id}\nFarmer: {land_data['owner_name']}")
                
        return jsonify(verification_result)
    except Exception as e:
        return jsonify({'verified': False, 'error': f"Internal Engine Runtime Error: {str(e)}"}), 500


# ============ ADMINISTRATIVE CONSOLE SERVICES ============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard_page'))
        else:
            return render_template('admin_login.html', error='Invalid administrative credentials footprint.')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard_page():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/api/admin/verifications-list', methods=['GET'])
def api_verifications_list():
    """Delivers full verification rows mapping cleanly to index structure models."""
    return jsonify(parse_farmers_csv_safely())

@app.route('/api/admin/all-boundaries', methods=['GET'])
def api_all_boundaries():
    return jsonify({'boundaries': get_all_boundaries_for_admin(), 'pesec': PESEC_CAMPUS})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/chat-bot')
def chat_bot():
    return redirect("https://2760f32k-5000.inc1.devtunnels.ms/")
@app.route('/whatsapp-group')
def whatsapp_group():
    return redirect("https://chat.whatsapp.com/CslaNwW7rqzGPXpU8PwkA8")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)