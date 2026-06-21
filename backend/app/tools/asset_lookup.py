import json
from pathlib import Path
from typing import Optional
from backend.app.models.schemas import AssetRecord

data_path = Path(__file__).resolve().parents[3] / "shared" / "data" / "asset_inventory.json"
with open(data_path) as f:
    data = json.load(f)
    ASSETS = data.get("assets", [])

def lookup_asset(ip: str, port: int) -> Optional[AssetRecord]:
    """
    Looks up an asset by IP and port in the asset inventory.
    Enforces the AssetRecord model contract.
    """
    port_val = int(port)
    
    # Try exact match on IP and port
    for asset in ASSETS:
        if asset.get("ip") == ip and asset.get("port") == port_val:
            return AssetRecord(
                asset_name=asset["name"],
                ip=asset["ip"],
                port=asset["port"],
                business_segment=asset.get("business_segment", "General"),
                record_count=asset.get("record_count", 0),
                data_sensitivity=asset.get("data_sensitivity", "LOW")
            )
            
    # Fallback to port match if IP is unknown or generic
    for asset in ASSETS:
        if asset.get("port") == port_val:
            return AssetRecord(
                asset_name=asset["name"],
                ip=asset["ip"],
                port=asset["port"],
                business_segment=asset.get("business_segment", "General"),
                record_count=asset.get("record_count", 0),
                data_sensitivity=asset.get("data_sensitivity", "LOW")
            )
            
    return None