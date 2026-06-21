import sys
import json
from unittest.mock import patch, MagicMock
from backend.app.agents.scout import scout_alert
from backend.app.agents.investigator import investigate_scout_output
from backend.app.agents.impact import assess_impact
from backend.app.agents.commander import generate_command
from backend.app.models.schemas import PipelineResults

def mock_httpx_post(url, *args, **kwargs):
    # Extract request payload
    json_data = kwargs.get("json", {})
    prompt = json_data.get("prompt", "")
    model = json_data.get("model", "")
    
    # Print out which model is being queried by the router
    print(f"   [Router Log] Outgoing request to model: {model} ...")
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    
    # Check agents in correct precedence
    if "Commander Agent" in prompt:
        if "Isolate affected servers immediately from the main VPC subnet." not in prompt:
            raise ValueError("Commander Agent prompt is missing playbook mitigation steps!")
        mock_resp.json.return_value = {
            "response": '{"summary_headline": "CRITICAL: RCE Attack Blocked on Production Struts Gateway", "recommended_actions": ["Isolate affected servers immediately from the main VPC subnet.", "Engage Incident Command Team and initiate P0 communication channel.", "Patch or rotate service credentials for affected machines."]}'
        }
    elif "Impact Agent" in prompt:
        if "Production Struts Gateway" not in prompt:
            raise ValueError("Impact Agent prompt is missing grounded asset information!")
        mock_resp.json.return_value = {
            "response": '{"severity": "CRITICAL", "affected_asset": "Production Struts Gateway", "potential_damage": "Total server compromise and potential lateral access to connected internal segments."}'
        }
    elif "Investigator Agent" in prompt:
        mock_resp.json.return_value = {
            "response": '{"diagnosis": "Apache Struts Remote Code Execution (RCE) attempt targeting web application v4.2", "confidence_score": 95}'
        }
    elif "Scout Agent" in prompt:
        mock_resp.json.return_value = {
            "response": '{"target": "10.0.0.150:8080", "attacker_ip": "198.51.100.42", "action": "Apache Struts Exploit on Port 8080"}'
        }
    else:
        mock_resp.json.return_value = {"response": "{}"}
        
    return mock_resp

def main():
    raw_alert = """
Critical Alert:
Unauthorized database access attempt via Apache Struts
on port 8080 from IP 198.51.100.42
"""

    print("=" * 60)
    print("RUNNING END-TO-END PIPELINE (SIMULATED OLLAMA, ACTUAL DB LOOKUPS)")
    print("=" * 60)

    with patch("httpx.Client.post", side_effect=mock_httpx_post):
        print("1. RUNNING SCOUT AGENT...")
        scout = scout_alert(raw_alert)
        print("SCOUT OUTPUT:")
        print(scout.model_dump_json(indent=2))
        print("-" * 40)

        print("2. RUNNING INVESTIGATOR AGENT...")
        investigation = investigate_scout_output(scout)
        print("INVESTIGATOR OUTPUT:")
        print(investigation.model_dump_json(indent=2))
        print("-" * 40)

        print("3. RUNNING IMPACT AGENT (Grounded in Tool Output)...")
        impact = assess_impact(scout, investigation)
        print("IMPACT OUTPUT:")
        print(impact.model_dump_json(indent=2))
        print("-" * 40)

        print("4. RUNNING COMMANDER AGENT (Grounded in Playbook Output)...")
        commander = generate_command(investigation, impact)
        print("COMMANDER OUTPUT:")
        print(commander.model_dump_json(indent=2))
        print("-" * 40)

        print("5. CONSTRUCTING FINAL PIPELINE ENVELOPE...")
        pipeline_results = PipelineResults(
            scout=scout,
            investigator=investigation,
            impact=impact,
            commander=commander
        )
        print("\nFINAL PIPELINE RESULTS JSON:")
        print(json.dumps(pipeline_results.model_dump(), indent=2))
        print("=" * 60)
        print("PIPELINE RUN COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()
