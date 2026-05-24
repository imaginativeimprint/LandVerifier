"""
Advanced GPS Extraction Module
Extracts and validates GPS data from images with high precision
"""

import io
import hashlib
import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import numpy as np
from typing import Tuple, Optional, Dict, Any

class GPSExtractor:
    """Advanced GPS extraction with validation"""
    
    def __init__(self):
        self.supported_formats = ['JPEG', 'PNG', 'TIFF']
    
    def extract_from_bytes(self, image_bytes: bytes) -> Optional[Tuple[float, float]]:
        """Extract GPS coordinates from image bytes"""
        try:
            # Use exifread for more reliable extraction
            tags = exifread.process_file(io.BytesIO(image_bytes), details=False)
            
            gps_lat = None
            gps_lon = None
            gps_lat_ref = None
            gps_lon_ref = None
            
            for tag, value in tags.items():
                if 'GPS GPSLatitude' in tag:
                    gps_lat = value.values
                elif 'GPS GPSLongitude' in tag:
                    gps_lon = value.values
                elif 'GPS GPSLatitudeRef' in tag:
                    gps_lat_ref = str(value)
                elif 'GPS GPSLongitudeRef' in tag:
                    gps_lon_ref = str(value)
            
            if gps_lat and gps_lon:
                lat = self._convert_to_degrees(gps_lat)
                lon = self._convert_to_degrees(gps_lon)
                
                if gps_lat_ref == 'S':
                    lat = -lat
                if gps_lon_ref == 'W':
                    lon = -lon
                
                return (lat, lon)
            
            # Fallback to PIL
            return self._extract_with_pil(image_bytes)
            
        except Exception as e:
            print(f"GPS extraction error: {e}")
            return None
    
    def _extract_with_pil(self, image_bytes: bytes) -> Optional[Tuple[float, float]]:
        """Extract GPS using PIL as fallback"""
        try:
            img = Image.open(io.BytesIO(image_bytes))
            exif_data = img._getexif()
            if not exif_data:
                return None
            
            exif = {TAGS.get(k, k): v for k, v in exif_data.items()}
            if "GPSInfo" not in exif:
                return None
            
            gps_info = {}
            for tag, value in exif["GPSInfo"].items():
                decoded = GPSTAGS.get(tag, tag)
                gps_info[decoded] = value
            
            lat = self._dms_to_decimal(
                gps_info["GPSLatitude"],
                gps_info["GPSLatitudeRef"]
            )
            lng = self._dms_to_decimal(
                gps_info["GPSLongitude"],
                gps_info["GPSLongitudeRef"]
            )
            
            return (lat, lng)
        except Exception as e:
            print(f"PIL GPS extraction error: {e}")
            return None
    
    def _convert_to_degrees(self, value) -> float:
        """Convert EXIF GPS coordinates to decimal degrees"""
        d = float(value[0].num) / float(value[0].den)
        m = float(value[1].num) / float(value[1].den)
        s = float(value[2].num) / float(value[2].den)
        return d + (m / 60.0) + (s / 3600.0)
    
    def _dms_to_decimal(self, dms, ref):
        """Convert DMS to decimal degrees"""
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
        decimal = degrees + minutes + seconds
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal
    
    def extract_with_validation(self, image_bytes: bytes) -> Dict[str, Any]:
        """Extract GPS with comprehensive validation"""
        result = {
            'success': False,
            'coordinates': None,
            'image_hash': None,
            'timestamp': None,
            'device_info': None,
            'message': ''
        }
        
        # Calculate image hash
        result['image_hash'] = hashlib.sha256(image_bytes).hexdigest()
        
        # Extract GPS
        coords = self.extract_from_bytes(image_bytes)
        
        if not coords:
            result['message'] = 'No GPS data found in image'
            return result
        
        lat, lng = coords
        
        # Validate coordinates are in Mandya region
        if not (12.40 <= lat <= 12.60) or not (76.80 <= lng <= 77.00):
            result['message'] = f'Coordinates outside Mandya region: {lat}, {lng}'
            return result
        
        result['success'] = True
        result['coordinates'] = (lat, lng)
        result['message'] = 'GPS extracted successfully'
        
        # Extract timestamp if available
        try:
            img = Image.open(io.BytesIO(image_bytes))
            exif_data = img._getexif()
            if exif_data and 306 in exif_data:  # DateTime tag
                result['timestamp'] = exif_data[306]
        except:
            pass
        
        return result


class GPSValidator:
    """GPS coordinate validation and processing"""
    
    @staticmethod
    def is_valid_coordinate(lat: float, lng: float) -> bool:
        """Check if coordinates are within valid ranges"""
        return -90 <= lat <= 90 and -180 <= lng <= 180
    
    @staticmethod
    def is_in_mandya_region(lat: float, lng: float) -> bool:
        """Check if coordinates are in Mandya region"""
        return (12.40 <= lat <= 12.60) and (76.80 <= lng <= 77.00)
    
    @staticmethod
    def calculate_accuracy_estimate(lat: float, lng: float, ref_lat: float, ref_lng: float) -> float:
        """Estimate GPS accuracy based on multiple factors"""
        from math import sqrt
        distance = sqrt((lat - ref_lat)**2 + (lng - ref_lng)**2) * 111000
        # Simple accuracy estimate (in production, use more factors)
        return min(100, max(5, distance * 0.1))
    
    @staticmethod
    def format_coordinates(lat: float, lng: float, format_type: str = 'dms') -> str:
        """Format coordinates in different formats"""
        if format_type == 'dms':
            lat_deg = int(abs(lat))
            lat_min = int((abs(lat) - lat_deg) * 60)
            lat_sec = ((abs(lat) - lat_deg) * 60 - lat_min) * 60
            lat_dir = 'N' if lat >= 0 else 'S'
            
            lng_deg = int(abs(lng))
            lng_min = int((abs(lng) - lng_deg) * 60)
            lng_sec = ((abs(lng) - lng_deg) * 60 - lng_min) * 60
            lng_dir = 'E' if lng >= 0 else 'W'
            
            return f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"{lat_dir} {lng_deg}°{lng_min}'{lng_sec:.1f}\"{lng_dir}"
        
        elif format_type == 'google':
            return f"{lat},{lng}"
        
        else:  # decimal
            return f"{lat:.6f}, {lng:.6f}"