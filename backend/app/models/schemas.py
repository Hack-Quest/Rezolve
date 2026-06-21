from pydantic import BaseModel
from typing import Literal, List

class ScoutOutput(BaseModel):
    target: str
    attacker_ip: str
    action: str

class InvestigatorOutput(BaseModel):
    diagnosis: str
    confidence_score: int

class ImpactOutput(BaseModel):
    severity: Literal[
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    ]
    affected_asset: str
    potential_damage: str

class CommanderOutput(BaseModel):
    summary_headline: str
    recommended_actions: List[str]

# Database/Tool Records
class CVERecord(BaseModel):
    id: str
    description: str
    cvss_score: float
    severity: str

class AssetRecord(BaseModel):
    asset_name: str
    ip: str
    port: int
    business_segment: str
    record_count: int
    data_sensitivity: str

class PlaybookResult(BaseModel):
    playbook_id: str
    steps: List[str]

# Pipeline Envelope Schema
class PipelineResults(BaseModel):
    scout: ScoutOutput
    investigator: InvestigatorOutput
    impact: ImpactOutput
    commander: CommanderOutput