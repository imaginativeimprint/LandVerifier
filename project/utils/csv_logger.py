"""
Advanced CSV Logging Module
Structured logging with analytics
"""

import csv
import os
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class CSVLogger:
    """Professional CSV logging with analytics"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.ensure_headers()
    
    def ensure_headers(self):
        """Create CSV with headers if not exists"""
        headers = [
            'Certificate_ID', 'Timestamp', 'Farmer_Name', 'Aadhar_Number',
            'Land_ID', 'Grid_Position', 'Captured_Latitude', 'Captured_Longitude',
            'Distance_Meters', 'Confidence_Score', 'Verification_Status',
            'VPN_Detected', 'IP_Address', 'Image_Hash', 'Processing_Time_MS'
        ]
        
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def log_verification(self, **kwargs):
        """Log a verification record"""
        row = [
            kwargs.get('certificate_id', ''),
            datetime.now().isoformat(),
            kwargs.get('farmer_name', ''),
            kwargs.get('aadhar', ''),
            kwargs.get('land_id', ''),
            kwargs.get('grid_position', ''),
            kwargs.get('latitude', 0),
            kwargs.get('longitude', 0),
            kwargs.get('distance', 0),
            kwargs.get('confidence', 0),
            kwargs.get('status', 'PENDING'),
            kwargs.get('vpn_detected', False),
            kwargs.get('ip_address', ''),
            kwargs.get('image_hash', ''),
            kwargs.get('processing_time', 0)
        ]
        
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        if not os.path.exists(self.filename):
            return {'total_verifications': 0}
        
        df = pd.read_csv(self.filename)
        
        total = len(df)
        approved = len(df[df['Verification_Status'] == 'APPROVED'])
        rejected = total - approved
        
        # Daily stats
        df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
        daily = df.groupby('Date').size().to_dict()
        
        # Crop distribution
        crop_stats = df.groupby('Crop_Type').size().to_dict() if 'Crop_Type' in df.columns else {}
        
        return {
            'total_verifications': total,
            'approved': approved,
            'rejected': rejected,
            'success_rate': round(approved / total * 100, 1) if total > 0 else 0,
            'daily_verifications': {str(k): v for k, v in daily.items()},
            'crop_distribution': crop_stats,
            'avg_distance': round(df['Distance_Meters'].mean(), 2) if total > 0 else 0,
            'avg_confidence': round(df['Confidence_Score'].mean(), 1) if total > 0 else 0
        }
    
    def get_farmer_stats(self, aadhar: str) -> Dict[str, Any]:
        """Get statistics for specific farmer"""
        if not os.path.exists(self.filename):
            return {'total': 0}
        
        df = pd.read_csv(self.filename)
        farmer_df = df[df['Aadhar_Number'] == aadhar]
        
        return {
            'total_verifications': len(farmer_df),
            'approved': len(farmer_df[farmer_df['Verification_Status'] == 'APPROVED']),
            'last_verification': farmer_df['Timestamp'].max() if len(farmer_df) > 0 else None,
            'avg_confidence': round(farmer_df['Confidence_Score'].mean(), 1) if len(farmer_df) > 0 else 0
        }
    
    def get_recent_verifications(self, limit: int = 20) -> List[Dict]:
        """Get recent verifications"""
        if not os.path.exists(self.filename):
            return []
        
        df = pd.read_csv(self.filename)
        df = df.sort_values('Timestamp', ascending=False).head(limit)
        
        return df.to_dict('records')
    
    def check_duplicate_hash(self, image_hash: str) -> bool:
        """Check if image hash already exists"""
        if not os.path.exists(self.filename):
            return False
        
        df = pd.read_csv(self.filename)
        return image_hash in df['Image_Hash'].values
    
    def export_to_excel(self, output_file: str):
        """Export to Excel format"""
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df.to_excel(output_file, index=False)
            return output_file
        return None
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive report"""
        stats = self.get_statistics()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': stats,
            'recent_verifications': self.get_recent_verifications(10)
        }
        
        # Save report as JSON
        report_file = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('reports', exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report


class AuditLogger:
    """Security audit logging"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
    
    def log_event(self, event_type: str, user_id: str, ip: str, details: str = None):
        """Log security event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'ip_address': ip,
            'details': details
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')