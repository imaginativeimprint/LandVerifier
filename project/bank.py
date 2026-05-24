"""
Bank Integration Module
Manages institutional investments, financial tiers, and document validation logic.
"""
import csv
import os
from datetime import datetime
from typing import List, Dict, Any

class BankingEngine:
    def __init__(self, ledger_file: str = 'verified_farmers.csv'):
        self.ledger_file = ledger_file
        self.max_income_threshold = 300000  # ₹3 Lakhs limit for low-net-worth small farmer subsidies

    def discover_stable_farmers(self) -> List[Dict[str, Any]]:
        """Parses the CSV log ledger to isolate high-confidence, physically verified farmers."""
        stable_farmers = {}
        if not os.path.exists(self.ledger_file):
            return []

        try:
            with open(self.ledger_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Isolate high confidence ratings (90%+) and stable physical farm presence
                    confidence = int(row.get('Confidence_Score', 0))
                    status = row.get('Verification_Status', '')
                    aadhar = row.get('Aadhar_Number', '')
                    
                    if confidence >= 90 and status == 'APPROVED':
                        # Use dict aggregation to keep only the latest record per unique farmer
                        stable_farmers[aadhar] = {
                            'farmer_name': row.get('Farmer_Name'),
                            'aadhar_masked': f"XXXX-XXXX-{aadhar[-4:]}" if aadhar else "XXXX-XXXX-XXXX",
                            'aadhar_raw': aadhar,
                            'land_id': row.get('Land_ID'),
                            'grid_position': row.get('Grid_Position'),
                            'confidence': confidence,
                            'vegetation_score': row.get('Vegetation_Density_Score', '0%'),
                            'last_verified': row.get('Timestamp', '').split('T')[0]
                        }
            return list(stable_farmers.values())
        except Exception:
            return []

    def evaluate_financial_eligibility(self, current_income: float) -> Dict[str, Any]:
        """Evaluates reported annual income against regional smallholder relief policy rules."""
        if current_income <= 0:
            return {'eligible': False, 'reason': 'Invalid or zero annual declaration income value.'}
            
        if current_income > self.max_income_threshold:
            return {
                'eligible': False,
                'reason': f"Annual income of ₹{current_income:,.2f} exceeds the smallholder maximum ceiling cap of ₹{self.max_income_threshold:,.2f}."
            }
            
        # Determine interest rate tier based on risk assessment profile
        if current_income <= 120000:
            tier = "Tier-1 Prime Agri-Relief"
            rate = "3.5% Per Annum"
            benefits = ["Zero Collateral Requirement", "Free Weather-Indexed Crop Insurance Backing", "₹50,000 Immediate Seed Capital Advance"]
        else:
            tier = "Tier-2 Standard Growth Support"
            rate = "5.5% Per Annum"
            benefits = ["Minimal Collateral (Land Token Asset)", "50% Subsidized Premium on Drone Surveying", "₹1,500,000 Maximum Modernization Credit Limit"]
            
        return {
            'eligible': True,
            'tier': tier,
            'interest_rate': rate,
            'benefits': benefits
        }