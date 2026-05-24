import csv
import json
import os

def process_bank_underwriting_ledger(csv_path="verified_farmers.csv"):
    """
    Scans the local verified_farmers ledger.
    Auto-discovers high-performance profiles eligible for micro-investment capital.
    """
    if not os.path.exists(csv_path):
        return {"error": f"Ledger database target missing: {csv_path}"}

    discovered_investment_profiles = []
    rejected_compliance_profiles = []

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            confidence = int(row['Confidence_Score'])
            income = int(row['Annual_Income'])
            status = row['Verification_Status']

            # Target Evaluation Rules:
            # Must pass OpenCV/Spatial telemetry and remain within the ₹3,00,000 subsidy ceiling
            if confidence >= 75 and income <= 300000 and status == "APPROVED":
                credit_tier = "PRIME_AGRI" if confidence >= 90 else "STANDARD_GROWTH"
                discovered_investment_profiles.append({
                    "id": row['Farmer_ID'],
                    "name": row['Farmer_Name'],
                    "crop": row['Crop_Type'],
                    "density": row['Vegetation_Density'],
                    "confidence": f"{confidence}%",
                    "income": f"₹{income:,}",
                    "assigned_tier": credit_tier,
                    "action": "EXTEND_INVESTMENT_PROPOSAL"
                })
            else:
                rejected_compliance_profiles.append({
                    "name": row['Farmer_Name'],
                    "reason": "Low Confidence Spatial Audit" if confidence < 75 else "Exceeds Income Policy Cap"
                })

    return {
        "active_ledger_source": csv_path,
        "discovered_pre_approved_profiles": discovered_investment_profiles,
        "flagged_compliance_failures": rejected_compliance_profiles
    }

# Quick validation runtime execution check
if __name__ == "__main__":
    results = process_bank_underwriting_ledger()
    print(json.dumps(results, indent=4))