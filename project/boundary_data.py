import math
from typing import List, Dict, Tuple, Optional

# ============================================
# PESEC COLLEGE CENTER & FINAL SHIFTED BOUNDS
# ============================================
# Shifted slightly South (down) and West (left) to align perfectly 
# with the exact pocket indicated by your reference layout mapping.

# Final adjusted southwest starting reference anchor
MIN_LAT = 12.5122  
MIN_LNG = 76.8740  

MATRIX_SIZE = 12  # Stays a perfect 12x12 grid
CELL_SIZE = 0.00075  # Sized to cleanly encompass the target sector fields

# Calculate boundaries stretching cleanly outward from the road intersections
MAX_LAT = MIN_LAT + (MATRIX_SIZE * CELL_SIZE)
MAX_LNG = MIN_LNG + (MATRIX_SIZE * CELL_SIZE)

# Recalculate center for campus relative mapping
PESEC_CENTER = {
    "lat": (MIN_LAT + MAX_LAT) / 2,
    "lng": (MIN_LNG + MAX_LNG) / 2
}

# ============================================
# 12x12 FARMER NAMES MATRIX (144 farmers)
# ============================================

FARMER_NAMES_LIST = [
    "Ramesh Gowda", "Lakshmamma", "Kumaraswamy", "Deve Gowda", "Nanjunda Swamy", "Putta Swamy",
    "Siddappa", "Mahadeva", "Basavaraj", "Shivanna", "Kempamma", "Chikkanna",
    "Nagamma", "Honnappa", "Eramma", "Mallesh", "Thimmanna", "Gowramma",
    "Chinnappa", "Lakshmi", "Murthy", "Prakash", "Shankar", "Radha",
    "Venkatesh", "Manjunath", "Sarojamma", "Ravindra", "Girijamma", "Suresh",
    "Jayamma", "Nagaraj", "Sharada", "Mohan", "Gangamma", "Krishnappa",
    "Kamalamma", "Srinivas", "Jayalakshmi", "Veeresh", "Parvathi", "Narayana",
    "Chandra", "Bhagyamma", "Shashidhar", "Rukmini", "Gopal", "Nirmala"
]

CROP_TYPES_LIST = [
    "Sugarcane", "Paddy", "Ragi", "Coconut", "Maize", "Banana",
    "Arecanut", "Cotton", "Groundnut", "Jowar", "Turmeric", "Pepper",
    "Sunflower", "Vegetables", "Flowers", "Wheat", "Pulses", "Oil Seeds",
    "Mango", "Cocoa", "Coffee", "Rubber", "Cashew", "Ginger",
    "Tobacco", "Cardamom", "Peas", "Beans", "Tomato", "Onion",
    "Potato", "Chili", "Brinjal", "Cabbage", "Cauliflower", "Spinach"
]

VILLAGE_LIST = [
    "Chandagalu", "Dodda Kere", "Hulikere", "Keragodu", "Mallenahalli", "Bharathipura",
    "Kerehosahalli", "Yelachagere", "Byadarahalli", "Heggere", "Koppa", "Kalenahalli",
    "Chikkahalli", "Hosahalli", "Gandhinagar", "Mudukatore", "Kikkeri", "Dudda",
    "Hallegere", "Arakere", "B G Nagara", "Hullenahalli", "Kyathanahalli", "Maranahalli"
]

# ============================================
# CREATE 12x12 MATRIX BOUNDARIES
# ============================================

def create_matrix_boundaries():
    """Create perfect 12x12 matrix/grid boundaries aligned to the shifted destination"""
    land_boundaries = {}
    
    # PESEC occupies center cells: rows 5-6, cols 5-6 (0-indexed)
    pesec_start_row = MATRIX_SIZE // 2 - 1  # 5
    pesec_end_row = pesec_start_row + 2      # 7
    pesec_start_col = MATRIX_SIZE // 2 - 1  # 5
    pesec_end_col = pesec_start_col + 2      # 7
    
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            # Skip PESEC campus cells (center 2x2 area)
            if (pesec_start_row <= row < pesec_end_row) and (pesec_start_col <= col < pesec_end_col):
                continue
            
            # Calculate cell bounds
            lat_min = MIN_LAT + (row * CELL_SIZE)
            lat_max = lat_min + CELL_SIZE
            lng_min = MIN_LNG + (col * CELL_SIZE)
            lng_max = lng_min + CELL_SIZE
            
            # Create rectangle polygon (perfect grid cell)
            polygon = [
                {"lat": lat_min, "lng": lng_min},
                {"lat": lat_min, "lng": lng_max},
                {"lat": lat_max, "lng": lng_max},
                {"lat": lat_max, "lng": lng_min},
                {"lat": lat_min, "lng": lng_min}
            ]
            
            # Calculate center
            center = {
                "lat": (lat_min + lat_max) / 2,
                "lng": (lng_min + lng_max) / 2
            }
            
            # Generate farmer name (cycle through list)
            idx = (row * MATRIX_SIZE + col) % len(FARMER_NAMES_LIST)
            farmer_name = FARMER_NAMES_LIST[idx]
            
            crop_type = CROP_TYPES_LIST[idx % len(CROP_TYPES_LIST)]
            village = VILLAGE_LIST[idx % len(VILLAGE_LIST)]
            
            # Standard secure placeholder unique string ID
            aadhar_placeholder = f"RED-ID-{row+1:02d}{col+1:02d}"
            
            # Calculate area in acres (approx based on cell layout scale)
            area_acres = round((CELL_SIZE * 111) ** 2 * 2.47, 2)
            
            # Generate land ID with matrix position
            land_id = f"PES-M{row+1:02d}{col+1:02d}"
            grid_position = f"R{row+1:02d}C{col+1:02d}"
            
            land_boundaries[land_id] = {
                "owner_aadhar": aadhar_placeholder,
                "owner_name": farmer_name,
                "area_acres": area_acres,
                "crop_type": crop_type,
                "village": village,
                "grid_position": grid_position,
                "row": row + 1,
                "col": col + 1,
                "polygon": polygon,
                "center": center,
                "active": True,
                "verified_count": 0
            }
    
    return land_boundaries

# Generate the 12x12 matrix
LAND_BOUNDARIES = create_matrix_boundaries()

# ============================================
# PESEC CAMPUS BOUNDARY (Center 2x2 block)
# ============================================

pesec_start_row = MATRIX_SIZE // 2 - 1
pesec_start_col = MATRIX_SIZE // 2 - 1

pesec_lat_min = MIN_LAT + (pesec_start_row * CELL_SIZE)
pesec_lat_max = pesec_lat_min + (2 * CELL_SIZE)
pesec_lng_min = MIN_LNG + (pesec_start_col * CELL_SIZE)
pesec_lng_max = pesec_lng_min + (2 * CELL_SIZE)

PESEC_CAMPUS = {
    "name": "PES College of Engineering, Mandya",
    "center": PESEC_CENTER,
    "polygon": [
        {"lat": pesec_lat_min, "lng": pesec_lng_min},
        {"lat": pesec_lat_min, "lng": pesec_lng_max},
        {"lat": pesec_lat_max, "lng": pesec_lng_max},
        {"lat": pesec_lat_max, "lng": pesec_lng_min},
        {"lat": pesec_lat_min, "lng": pesec_lng_min}
    ],
    "grid_position": f"CENTER (R{pesec_start_row+1:02d}C{pesec_start_col+1:02d} to R{pesec_start_row+2:02d}C{pesec_start_col+2:02d})",
    "landmarks": ["Main Building", "Library", "Canteen", "Playground", "Agriculture Dept", "Hostel", "Sports Ground"]
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def point_in_polygon(point_lat: float, point_lng: float, polygon: List[Dict]) -> bool:
    x = point_lng
    y = point_lat
    inside = False
    n = len(polygon)
    
    for i in range(n):
        x1 = polygon[i]['lng']
        y1 = polygon[i]['lat']
        x2 = polygon[(i + 1) % n]['lng']
        y2 = polygon[(i + 1) % n]['lat']
        
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside
    
    return inside

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_land_by_coordinates(lat: float, lng: float) -> Tuple[Optional[str], Optional[Dict]]:
    if point_in_polygon(lat, lng, PESEC_CAMPUS['polygon']):
        return "PESEC_CAMPUS", PESEC_CAMPUS
    
    for land_id, land_data in LAND_BOUNDARIES.items():
        if point_in_polygon(lat, lng, land_data['polygon']):
            return land_id, land_data
    return None, None

def get_land_by_aadhar(aadhar: str) -> Tuple[Optional[str], Optional[Dict]]:
    for land_id, land_data in LAND_BOUNDARIES.items():
        if land_data['owner_aadhar'] == aadhar:
            return land_id, land_data
    return None, None

def get_all_boundaries_for_admin() -> List[Dict]:
    boundaries = []
    for land_id, land_data in LAND_BOUNDARIES.items():
        boundaries.append({
            'id': land_id,
            'owner_name': land_data['owner_name'],
            'owner_aadhar': land_data['owner_aadhar'],
            'area_acres': land_data['area_acres'],
            'crop_type': land_data['crop_type'],
            'village': land_data['village'],
            'grid_position': land_data['grid_position'],
            'row': land_data['row'],
            'col': land_data['col'],
            'polygon': land_data['polygon'],
            'center': land_data['center']
        })
    return boundaries

def get_boundary_statistics() -> Dict:
    total_lands = len(LAND_BOUNDARIES)
    total_acres = sum(l['area_acres'] for l in LAND_BOUNDARIES.values())
    
    crop_stats = {}
    for land in LAND_BOUNDARIES.values():
        crop = land['crop_type']
        crop_stats[crop] = crop_stats.get(crop, 0) + 1
    
    return {
        'total_lands': total_lands,
        'total_acres': round(total_acres, 1),
        'avg_area_acres': round(total_acres / total_lands, 2),
        'crop_distribution': crop_stats,
        'matrix_size': f"{MATRIX_SIZE}x{MATRIX_SIZE}"
    }

# ============================================
# MISSING FUNCTIONS FOR COMPATIBILITY
# ============================================

def calculate_polygon_area_sqkm(polygon: List[Dict]) -> float:
    n = len(polygon)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i]['lat'] * polygon[j]['lng']
        area -= polygon[j]['lat'] * polygon[i]['lng']
    area = abs(area) / 2
    return area * 111 * 111 / 1000000

calculate_polygon_area = calculate_polygon_area_sqkm

def calculate_polygon_center(polygon: List[Dict]) -> Dict:
    lats = [p['lat'] for p in polygon]
    lngs = [p['lng'] for p in polygon]
    return {
        "lat": sum(lats) / len(lats),
        "lng": sum(lngs) / len(lngs)
    }

def get_adjacent_boundaries(land_id: str) -> List[Dict]:
    return []

def search_lands_by_crop(crop_type: str) -> List[Dict]:
    results = []
    for land_id, land_data in LAND_BOUNDARIES.items():
        if land_data['crop_type'].lower() == crop_type.lower():
            results.append({
                'land_id': land_id,
                'owner': land_data['owner_name'],
                'area': land_data['area_acres'],
                'grid': land_data['grid_position']
            })
    return results

def search_lands_by_village(village: str) -> List[Dict]:
    results = []
    for land_id, land_data in LAND_BOUNDARIES.items():
        if land_data['village'].lower() == village.lower():
            results.append({
                'land_id': land_id,
                'owner': land_data['owner_name'],
                'crop': land_data['crop_type'],
                'grid': land_data['grid_position']
            })
    return results

# ============================================
# PRINT 12x12 MATRIX VISUALIZATION
# ============================================

print("=" * 80)
print("📍 FINAL ADJUSTED 12x12 MATRIX - TARGET CORRIDOR DROPPED POSITION")
print("=" * 80)
print(f"Matrix Bounds South-West Anchor: {MIN_LAT:.4f}, {MIN_LNG:.4f}")
print(f"Matrix Bounds North-East Corner: {MAX_LAT:.4f}, {MAX_LNG:.4f}")
print(f"Active Blocks: {len(LAND_BOUNDARIES)} (PESEC occupies center 2x2 cells)")
print(f"Cell Size: ~{CELL_SIZE * 111:.0f} meters per block side")
print(f"Total Combined Grid Area: {get_boundary_statistics()['total_acres']:.0f} acres")
print("=" * 80)

print("\n🗺️ 12x12 SHIFTED LAYOUT (🏫=PESEC):")
print("     C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12")
for row in range(MATRIX_SIZE):
    row_label = f"R{row+1:02d}"
    row_display = []
    pesec_start_row = MATRIX_SIZE // 2 - 1
    pesec_end_row = pesec_start_row + 2
    pesec_start_col = MATRIX_SIZE // 2 - 1
    pesec_end_col = pesec_start_col + 2
    
    for col in range(MATRIX_SIZE):
        if (pesec_start_row <= row < pesec_end_row) and (pesec_start_col <= col < pesec_end_col):
            row_display.append(" 🏫 ")
        else:
            land_id = f"PES-M{row+1:02d}{col+1:02d}"
            if land_id in LAND_BOUNDARIES:
                farmer_first = LAND_BOUNDARIES[land_id]['owner_name'][0]
                row_display.append(f" {farmer_first}  ")
            else:
                row_display.append(" -  ")
    print(f"{row_label} {''.join(row_display)}")

# ============================================
# EXPORTS
# ============================================

__all__ = [
    'LAND_BOUNDARIES',
    'PESEC_CAMPUS',
    'find_land_by_coordinates',
    'get_land_by_aadhar',
    'point_in_polygon',
    'haversine_distance',
    'get_all_boundaries_for_admin',
    'get_boundary_statistics',
    'get_adjacent_boundaries',
    'search_lands_by_crop',
    'search_lands_by_village',
    'calculate_polygon_area_sqkm',
    'calculate_polygon_area',
    'calculate_polygon_center'
]