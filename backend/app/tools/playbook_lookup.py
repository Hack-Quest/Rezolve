import json
from pathlib import Path
from typing import Optional
from backend.app.models.schemas import PlaybookResult

data_path = Path(__file__).resolve().parents[3] / "shared" / "data" / "playbooks.json"
with open(data_path) as f:
    PLAYBOOKS = json.load(f)

def lookup_playbook(severity: str) -> Optional[PlaybookResult]:
    """
    Looks up a playbook by severity or specific threat type (e.g., 'CRITICAL', 'SQL_INJECTION').
    Enforces the PlaybookResult model contract.
    """
    key = severity.strip().upper()
    playbook_data = PLAYBOOKS.get(key)
    
    if playbook_data:
        return PlaybookResult(
            playbook_id=playbook_data["playbook_id"],
            steps=playbook_data["steps"]
        )
        
    # Fallback default if not found
    return PlaybookResult(
        playbook_id="PB-GEN-01",
        steps=[
            "Isolate the system and review logs.",
            "Alert on-call security engineer.",
            "Verify mitigation controls are active."
        ]
    )