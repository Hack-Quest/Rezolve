"""
test_pipeline.py — Run the 4-agent pipeline against any sample alert.

Usage:
    python test_pipeline.py              # picks ONE random alert
    python test_pipeline.py alert-003    # runs alert-003 (specific)
    python test_pipeline.py --all        # runs all alerts sequentially
    python test_pipeline.py --random 5   # runs 5 random alerts (no repeats)

This script reads from shared/data/sample_alerts.json so you can test
every demo scenario without editing code.
"""
import sys
import json
import logging
import time
import random
from pathlib import Path
from backend.app.agents.scout import scout_alert
from backend.app.agents.investigator import investigate_scout_output
from backend.app.agents.impact import assess_impact
from backend.app.agents.commander import generate_command
from backend.app.models.schemas import PipelineResults

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Path to the sample alerts file
ALERTS_FILE = Path(__file__).resolve().parent / "shared" / "data" / "sample_alerts.json"


def load_alerts() -> list[dict]:
    """Load all sample alerts from the JSON file."""
    with open(ALERTS_FILE) as f:
        data = json.load(f)
    return data["alerts"]


def find_alert(alert_id: str) -> dict:
    """Find a single alert by its ID (e.g., 'alert-001')."""
    alerts = load_alerts()
    for alert in alerts:
        if alert["id"] == alert_id:
            return alert
    available = ", ".join(a["id"] for a in alerts)
    raise ValueError(f"Alert '{alert_id}' not found. Available: {available}")


def run_pipeline(raw_alert: str) -> PipelineResults:
    """
    Run the full 4-agent pipeline on a raw alert string.
    Returns a PipelineResults envelope.
    
    P3 can import this function directly to wrap in FastAPI.
    """
    scout = scout_alert(raw_alert)
    investigator = investigate_scout_output(scout)
    impact = assess_impact(scout, investigator, raw_alert)
    commander = generate_command(investigator, impact)
    return PipelineResults(
        scout=scout,
        investigator=investigator,
        impact=impact,
        commander=commander,
    )


def run_single_alert(alert: dict) -> bool:
    """Run the pipeline on one alert, print results, return True on success."""
    print("=" * 60)
    print(f"ALERT: {alert['id']} | {alert['severity']} | {alert['title']}")
    print(f"Expected asset: {alert.get('expected_asset', 'N/A')}")
    print(f"Expected playbook: {alert.get('expected_playbook', 'N/A')}")
    print("=" * 60)
    print(f"RAW ALERT:\n{alert['raw_log']}")
    print("-" * 60)

    start_time = time.time()
    try:
        results = run_pipeline(alert["raw_log"])
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n[FAILED in {elapsed:.1f}s] {type(e).__name__}: {e}")
        return False

    elapsed = time.time() - start_time
    print(f"\nPIPELINE RESULTS (completed in {elapsed:.1f}s):")
    print(json.dumps(results.model_dump(), indent=2))

    # Verification — did the pipeline find the expected asset?
    actual_asset = results.impact.affected_asset
    expected_asset = alert.get("expected_asset")
    if expected_asset and actual_asset == expected_asset:
        print(f"\n✓ Asset match: {actual_asset}")
    elif expected_asset:
        print(f"\n✗ Asset mismatch — expected '{expected_asset}', got '{actual_asset}'")

    print("\n" + "=" * 60)
    print(f"SUCCESS — {alert['id']} completed in {elapsed:.1f}s")
    return True


def print_summary(results: list[tuple[str, bool]]) -> None:
    """Print a pass/fail summary for a batch of runs."""
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for alert_id, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {alert_id}: {status}")
    
    total_pass = sum(1 for _, s in results if s)
    print(f"\n{total_pass}/{len(results)} alerts passed")


def main():
    args = sys.argv[1:]

    # --- python test_pipeline.py --all ---
    # Run every alert in the file, sequentially.
    if args and args[0] == "--all":
        alerts = load_alerts()
        print(f"Running all {len(alerts)} sample alerts sequentially...\n")
        results = []
        for alert in alerts:
            success = run_single_alert(alert)
            results.append((alert["id"], success))
            print("\n")
        print_summary(results)
        sys.exit(0 if all(s for _, s in results) else 1)

    # --- python test_pipeline.py --random [N] ---
    # Run N random alerts (default 1), no repeats within the batch.
    # Useful for stochastic testing without running the full 50-alert suite.
    if args and args[0] == "--random":
        n = int(args[1]) if len(args) > 1 else 1
        alerts = load_alerts()
        if n > len(alerts):
            print(f"Warning: requested {n} but only {len(alerts)} alerts available — running all")
            n = len(alerts)
        chosen = random.sample(alerts, n)
        print(f"Running {n} random alert(s) from {len(alerts)} total...\n")
        results = []
        for alert in chosen:
            success = run_single_alert(alert)
            results.append((alert["id"], success))
            print("\n")
        print_summary(results)
        sys.exit(0 if all(s for _, s in results) else 1)

    # --- python test_pipeline.py alert-003 ---
    # Run a specific alert by ID.
    if args and args[0].startswith("alert-"):
        alert_id = args[0]
        try:
            alert = find_alert(alert_id)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        success = run_single_alert(alert)
        sys.exit(0 if success else 1)

    # --- python test_pipeline.py (no args) ---
    # Default: pick ONE random alert. Good for quick smoke tests.
    alerts = load_alerts()
    alert = random.choice(alerts)
    print(f"Random alert selected: {alert['id']}")
    print("Usage: python test_pipeline.py [alert-001|alert-002|...|--all|--random N]")
    print()
    success = run_single_alert(alert)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()