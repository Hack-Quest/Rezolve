import json
from pathlib import Path
from typing import Optional
from backend.app.models.schemas import CVERecord

data_path = Path(__file__).resolve().parents[3] / "shared" / "data" / "cve_database.json"
with open(data_path) as f:
    CVES = json.load(f)

def lookup_cve(cve_id: str) -> Optional[CVERecord]:
    """
    Looks up a CVE in the database by CVE ID.
    Falls back to searching keywords in description if not found by exact ID.
    Enforces the CVERecord model contract.
    """
    if not cve_id:
        return None
        
    cve_id_clean = cve_id.strip()
    
    # Try exact match by key (case-insensitive)
    for key, val in CVES.items():
        if key.lower() == cve_id_clean.lower():
            return CVERecord(
                id=val["id"],
                description=val["description"],
                cvss_score=val["cvss_score"],
                severity=val["severity"]
            )
            
    # Fallback: search in description or keys
    for key, val in CVES.items():
        if cve_id_clean.lower() in key.lower() or cve_id_clean.lower() in val.get("description", "").lower():
            return CVERecord(
                id=val["id"],
                description=val["description"],
                cvss_score=val["cvss_score"],
                severity=val["severity"]
            )
            
    return None
