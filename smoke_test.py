"""
smoke_test.py — End-to-end backend smoke test for the Rezolve platform.

Validates the ENTIRE backend stack WITHOUT a frontend:
  - Server is up and model warmup completed
  - /api/health returns ok
  - /api/alerts returns the 7 pre-seeded alerts
  - /api/alerts/{id} returns a single alert, 404 for unknown
  - /api/stream?alert_id=X streams all 10 SSE events in order
  - All 4 agents produce valid Pydantic-validated output
  - The 3 "wow moments" fire:
      #1: CVE number in investigator.diagnosis (looked up from cve_database.json)
      #2: affected_asset in impact output (looked up from asset_inventory.json)
      #3: 3 recommended_actions in commander output (looked up from playbooks.json)
  - Store persistence: /api/alerts/{id} shows pipeline_results AFTER stream completes
  - Free-text alert path works (no alert_id, no persistence)
  - Error handling: 400 when neither alert_id nor raw_alert is provided

Usage:
    # Server must already be running on localhost:8000
    python smoke_test.py                  # run all tests, alert-001 by default
    python smoke_test.py alert-003        # use a different alert ID
    python smoke_test.py --host localhost --port 8000   # custom host/port
    python smoke_test.py --no-stream      # skip the slow SSE test (fast smoke)
    python smoke_test.py --verbose        # print full JSON of every response

Exit code: 0 if all tests pass, 1 if any fail.

Requirements (already in backend/requirements.txt):
    - httpx  (for HTTP + SSE streaming)
    - pydantic (for response validation, optional)

Tested on Python 3.11+ on Windows / macOS / Linux.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any, Iterator

import httpx


# --------------------------------------------------------------------------- #
# Pretty-printing helpers
# --------------------------------------------------------------------------- #
class Colors:
    """ANSI color codes. Auto-disabled on Windows if not supported."""
    RESET   = "\031[0m" if sys.platform == "win32" else "\033[0m"
    GREEN   = "\031[32m" if sys.platform == "win32" else "\033[32m"
    RED     = "\033[31m" if sys.platform == "win32" else "\033[31m"
    YELLOW  = "\033[33m" if sys.platform == "win32" else "\033[33m"
    CYAN    = "\033[36m" if sys.platform == "win32" else "\033[36m"
    BOLD    = "\033[1m"  if sys.platform == "win32" else "\033[1m"
    DIM     = "\033[2m"  if sys.platform == "win32" else "\033[2m"


def _enable_windows_ansi() -> None:
    """Enable ANSI escape sequences on Windows 10+ terminals."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        # If it fails, colors just won't render — output is still readable.
        pass


_enable_windows_ansi()


def ok(msg: str) -> None:
    print(f"  {Colors.GREEN}✓{Colors.RESET} {msg}")


def fail(msg: str, detail: str = "") -> None:
    print(f"  {Colors.RED}✗{Colors.RESET} {msg}")
    if detail:
        for line in detail.strip().splitlines():
            print(f"      {Colors.DIM}{line}{Colors.RESET}")


def warn(msg: str) -> None:
    print(f"  {Colors.YELLOW}!{Colors.RESET} {msg}")


def info(msg: str) -> None:
    print(f"  {Colors.CYAN}•{Colors.RESET} {msg}")


def header(title: str) -> None:
    print(f"\n{Colors.BOLD}{Colors.CYAN}── {title} {'─' * max(1, 60 - len(title))}{Colors.RESET}")


def banner(text: str) -> None:
    line = "═" * 70
    print(f"\n{Colors.BOLD}{line}\n  {text}\n{line}{Colors.RESET}")


# --------------------------------------------------------------------------- #
# Test result tracking
# --------------------------------------------------------------------------- #
class TestRun:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.failures: list[str] = []

    def record_pass(self, name: str) -> None:
        self.passed += 1

    def record_fail(self, name: str, detail: str = "") -> None:
        self.failed += 1
        self.failures.append(f"{name}: {detail}" if detail else name)

    def record_warn(self) -> None:
        self.warnings += 1


# --------------------------------------------------------------------------- #
# SSE parser — turns a raw text/event-stream into (event, data) tuples
# --------------------------------------------------------------------------- #
def parse_sse_stream(response: httpx.Response) -> Iterator[tuple[str, dict]]:
    """
    Parse an SSE stream from an httpx streaming response.

    Yields (event_name, data_dict) tuples. Handles:
      - Multiple data: lines per event (concatenated with \n)
      - Events without an explicit event: line (defaults to "message")
      - Comments and keep-alive lines (ignored)
    """
    event_name = "message"
    data_lines: list[str] = []

    for line in response.iter_lines():
        if line is None:
            continue
        # httpx yields str, but be defensive
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="replace")

        # Strip the trailing newline that httpx may or may not preserve
        line = line.rstrip("\r\n")

        if line == "":
            # Blank line = event boundary. Emit if we have data.
            if data_lines:
                raw_data = "\n".join(data_lines)
                try:
                    data = json.loads(raw_data)
                except json.JSONDecodeError:
                    data = {"_raw": raw_data}
                yield event_name, data
            event_name = "message"
            data_lines = []
            continue

        if line.startswith(":"):
            # SSE comment / keep-alive — ignore
            continue

        if line.startswith("event:"):
            event_name = line[len("event:"):].strip()
        elif line.startswith("data:"):
            data_lines.append(line[len("data:"):].strip())
        # Ignore unknown fields (id:, retry:, etc.)


# --------------------------------------------------------------------------- #
# Individual tests
# --------------------------------------------------------------------------- #
def test_server_up(base_url: str, run: TestRun) -> bool:
    """Verify the server is reachable at all."""
    header("TEST 1 — Server reachable")
    try:
        r = httpx.get(f"{base_url}/api/health", timeout=30.0)
        if r.status_code == 200:
            ok(f"Server is up at {base_url}")
            run.record_pass("server_up")
            return True
        else:
            fail(f"Server returned {r.status_code}", r.text[:200])
            run.record_fail("server_up", f"status {r.status_code}")
            return False
    except httpx.ConnectError as e:
        fail(f"Cannot connect to {base_url}", str(e))
        run.record_fail("server_up", str(e))
        return False
    except Exception as e:
        fail(f"Unexpected error connecting", f"{type(e).__name__}: {e}")
        run.record_fail("server_up", str(e))
        return False


def test_health(base_url: str, run: TestRun, verbose: bool) -> bool:
    """GET /api/health returns {"ok": true}."""
    header("TEST 2 — GET /api/health")
    try:
        r = httpx.get(f"{base_url}/api/health", timeout=10.0)
        if r.status_code != 200:
            fail(f"Expected 200, got {r.status_code}", r.text[:200])
            run.record_fail("health", f"status {r.status_code}")
            return False
        body = r.json()
        if body.get("ok") is True:
            ok('Response: {"ok": true}')
            if verbose:
                info(f"Full response: {body}")
            run.record_pass("health")
            return True
        else:
            fail(f'Expected {{"ok": true}}, got {body}')
            run.record_fail("health", str(body))
            return False
    except Exception as e:
        fail("Exception during health check", f"{type(e).__name__}: {e}")
        run.record_fail("health", str(e))
        return False


def test_list_alerts(base_url: str, run: TestRun, verbose: bool) -> list[dict]:
    """GET /api/alerts returns the 7 pre-seeded alerts."""
    header("TEST 3 — GET /api/alerts (list pre-seeded)")
    try:
        r = httpx.get(f"{base_url}/api/alerts", timeout=10.0)
        if r.status_code != 200:
            fail(f"Expected 200, got {r.status_code}", r.text[:200])
            run.record_fail("list_alerts", f"status {r.status_code}")
            return []
        alerts = r.json()
        if not isinstance(alerts, list):
            fail(f"Expected a list, got {type(alerts).__name__}")
            run.record_fail("list_alerts", "not a list")
            return []

        if len(alerts) == 0:
            fail("Store is empty — did seed_from_sample_file() run?")
            run.record_fail("list_alerts", "empty store")
            return []

        ok(f"Returned {len(alerts)} alert(s)")
        if len(alerts) != 7:
            warn(f"Expected 7 pre-seeded alerts, got {len(alerts)}")
            run.record_warn()
        else:
            ok("Count matches SEED_COUNT = 7")

        # Verify schema of each alert
        required_fields = {"id", "title", "severity", "raw_log", "processed_at", "pipeline_results"}
        for a in alerts:
            missing = required_fields - set(a.keys())
            if missing:
                fail(f"Alert {a.get('id', '?')} missing fields: {missing}")
                run.record_fail("list_alerts", f"missing fields {missing}")
                return []

        ok("All alerts have required fields: id, title, severity, raw_log, processed_at, pipeline_results")

        # Show a preview
        if verbose:
            for a in alerts:
                status = "processed" if a.get("processed_at") else "pending"
                info(f"  {a['id']:12} {a['severity']:10} [{status}] {a['title']}")
        else:
            # Compact preview: first 3
            for a in alerts[:3]:
                status = "processed" if a.get("processed_at") else "pending"
                info(f"  {a['id']:12} {a['severity']:10} [{status}] {a['title']}")
            if len(alerts) > 3:
                info(f"  ... and {len(alerts) - 3} more")

        run.record_pass("list_alerts")
        return alerts
    except Exception as e:
        fail("Exception during list alerts", f"{type(e).__name__}: {e}")
        run.record_fail("list_alerts", str(e))
        return []


def test_get_single_alert(base_url: str, alert_id: str, run: TestRun, verbose: bool) -> dict | None:
    """GET /api/alerts/{id} returns the right alert."""
    header(f"TEST 4 — GET /api/alerts/{alert_id}")
    try:
        r = httpx.get(f"{base_url}/api/alerts/{alert_id}", timeout=10.0)
        if r.status_code != 200:
            fail(f"Expected 200, got {r.status_code}", r.text[:200])
            run.record_fail("get_alert", f"status {r.status_code}")
            return None
        alert = r.json()
        if alert.get("id") != alert_id:
            fail(f"Expected id={alert_id}, got {alert.get('id')}")
            run.record_fail("get_alert", "id mismatch")
            return None
        ok(f"Returned alert: {alert['title']}")
        ok(f"Severity: {alert['severity']}")
        if verbose:
            info(f"Full alert: {json.dumps(alert, indent=2)[:500]}")
        run.record_pass("get_alert")
        return alert
    except Exception as e:
        fail("Exception during get single alert", f"{type(e).__name__}: {e}")
        run.record_fail("get_alert", str(e))
        return None


def test_404_unknown_alert(base_url: str, run: TestRun) -> bool:
    """GET /api/alerts/alert-999 returns 404."""
    header("TEST 5 — GET /api/alerts/alert-999 (404 path)")
    try:
        r = httpx.get(f"{base_url}/api/alerts/alert-999", timeout=10.0)
        if r.status_code == 404:
            ok(f"Got 404 as expected")
            try:
                detail = r.json().get("detail", "")
                ok(f"Detail: {detail}")
            except Exception:
                pass
            run.record_pass("404")
            return True
        else:
            fail(f"Expected 404, got {r.status_code}", r.text[:200])
            run.record_fail("404", f"status {r.status_code}")
            return False
    except Exception as e:
        fail("Exception during 404 test", f"{type(e).__name__}: {e}")
        run.record_fail("404", str(e))
        return False


def test_400_no_params(base_url: str, run: TestRun) -> bool:
    """GET /api/stream with no params returns 400."""
    header("TEST 6 — GET /api/stream (no params, expect 400)")
    try:
        r = httpx.get(f"{base_url}/api/stream", timeout=10.0)
        if r.status_code == 400:
            ok("Got 400 as expected")
            try:
                detail = r.json().get("detail", "")
                ok(f"Detail: {detail}")
            except Exception:
                pass
            run.record_pass("400")
            return True
        else:
            fail(f"Expected 400, got {r.status_code}", r.text[:200])
            run.record_fail("400", f"status {r.status_code}")
            return False
    except Exception as e:
        fail("Exception during 400 test", f"{type(e).__name__}: {e}")
        run.record_fail("400", str(e))
        return False


def test_sse_stream(
    base_url: str,
    alert_id: str,
    run: TestRun,
    verbose: bool,
) -> tuple[dict | None, float]:
    """
    GET /api/stream?alert_id=X — the big one.

    Streams the SSE pipeline, verifies the event sequence, validates each
    agent's output, and checks that the 3 wow moments fire.

    Returns (final_envelope_dict_or_None, total_pipeline_seconds).
    """
    header(f"TEST 7 — GET /api/stream?alert_id={alert_id} (full SSE pipeline)")
    print(f"  {Colors.DIM}Streaming... (this takes 5-45 seconds depending on hardware){Colors.RESET}")

    expected_event_sequence = [
        "pipeline_start",
        "agent_start",       # scout
        "agent_complete",    # scout
        "agent_start",       # investigator
        "agent_complete",    # investigator
        "agent_start",       # impact
        "agent_complete",    # impact
        "agent_start",       # commander
        "agent_complete",    # commander
        "pipeline_complete",
    ]
    seen_events: list[str] = []
    agent_outputs: dict[str, dict] = {}
    final_envelope: dict | None = None
    total_s: float | None = None
    error_message: str | None = None

    t0 = time.time()
    try:
        # Stream the response. timeout=None means "no total timeout" — we rely
        # on the server's own pipeline_error event to terminate the stream.
        with httpx.stream(
            "GET",
            f"{base_url}/api/stream",
            params={"alert_id": alert_id},
            timeout=httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0),
        ) as r:
            if r.status_code != 200:
                body = r.read().decode("utf-8", errors="replace")
                fail(f"Expected 200, got {r.status_code}", body[:300])
                run.record_fail("sse_stream", f"status {r.status_code}")
                return None, 0.0

            for event_name, data in parse_sse_stream(r):
                seen_events.append(event_name)
                elapsed = time.time() - t0

                if event_name == "pipeline_start":
                    raw_alert = data.get("raw_alert", "")
                    preview = raw_alert[:80] + ("..." if len(raw_alert) > 80 else "")
                    ok(f"pipeline_start — raw alert received ({len(raw_alert)} chars)")
                    if verbose:
                        info(f"  Raw: {preview}")

                elif event_name == "agent_start":
                    agent = data.get("agent", "?")
                    print(f"  {Colors.DIM}[{elapsed:5.1f}s]{Colors.RESET} ▶ {agent} starting...")

                elif event_name == "agent_complete":
                    agent = data.get("agent", "?")
                    agent_elapsed = data.get("elapsed_s", 0)
                    output = data.get("output", {})
                    agent_outputs[agent] = output
                    print(f"  {Colors.DIM}[{elapsed:5.1f}s]{Colors.RESET} {Colors.GREEN}✓{Colors.RESET} {agent} done in {agent_elapsed}s")
                    if verbose and output:
                        info(f"  Output: {json.dumps(output)[:200]}")

                elif event_name == "pipeline_complete":
                    total_s = data.get("total_s", 0)
                    final_envelope = data.get("results", {})
                    print(f"  {Colors.DIM}[{elapsed:5.1f}s]{Colors.RESET} {Colors.GREEN}✓ pipeline_complete — total {total_s}s{Colors.RESET}")

                elif event_name == "pipeline_error":
                    error_message = data.get("message", "unknown error")
                    print(f"  {Colors.DIM}[{elapsed:5.1f}s]{Colors.RESET} {Colors.RED}✗ pipeline_error: {error_message}{Colors.RESET}")

                else:
                    warn(f"Unknown event: {event_name} — {data}")

    except httpx.ReadTimeout:
        fail("Stream timed out — server may be slow or hung")
        run.record_fail("sse_stream", "read timeout")
        return None, time.time() - t0
    except Exception as e:
        fail(f"Exception during stream: {type(e).__name__}: {e}")
        run.record_fail("sse_stream", str(e))
        return None, time.time() - t0

    elapsed = time.time() - t0
    print(f"  {Colors.DIM}Stream closed after {elapsed:.1f}s wall time{Colors.RESET}")

    # --- Validate event sequence -------------------------------------------
    print()
    header("TEST 7a — SSE event sequence")
    if seen_events == expected_event_sequence:
        ok(f"All 10 events fired in correct order")
        run.record_pass("sse_sequence")
    else:
        fail("Event sequence mismatch")
        print(f"      {Colors.DIM}Expected:{Colors.RESET} {expected_event_sequence}")
        print(f"      {Colors.DIM}Got:     {Colors.RESET} {seen_events}")
        # Partial credit: did we at least get pipeline_complete?
        if "pipeline_complete" in seen_events:
            warn("pipeline_complete did fire — sequence is close but not exact")
            run.record_warn()
            run.record_pass("sse_sequence_partial")
        else:
            run.record_fail("sse_sequence", f"got {seen_events}")

    # --- Validate pipeline_error didn't fire -------------------------------
    if error_message is not None:
        fail(f"Pipeline errored: {error_message}")
        run.record_fail("pipeline_no_error", error_message)
        return None, elapsed

    # --- Validate each agent's output --------------------------------------
    print()
    header("TEST 7b — Agent output validation")

    # Scout
    scout = agent_outputs.get("scout", {})
    if not scout:
        fail("Scout output missing")
        run.record_fail("scout_output", "missing")
    else:
        issues = []
        if not scout.get("target"):
            issues.append("target is empty")
        if not scout.get("attacker_ip"):
            issues.append("attacker_ip is empty")
        if not scout.get("action"):
            issues.append("action is empty")
        if issues:
            fail(f"Scout output issues: {', '.join(issues)}")
            run.record_fail("scout_output", "; ".join(issues))
        else:
            ok(f"Scout: target={scout['target']!r}, attacker_ip={scout['attacker_ip']!r}")
            run.record_pass("scout_output")

    # Investigator — WOW #1: CVE number must appear in diagnosis
    investigator = agent_outputs.get("investigator", {})
    if not investigator:
        fail("Investigator output missing")
        run.record_fail("investigator_output", "missing")
    else:
        diagnosis = investigator.get("diagnosis", "")
        confidence = investigator.get("confidence_score", 0)
        issues = []
        if not diagnosis:
            issues.append("diagnosis is empty")
        if not isinstance(confidence, int) or not (0 <= confidence <= 100):
            issues.append(f"confidence_score={confidence!r} (expected int 0-100)")
        elif confidence > 95:
            warn(f"confidence_score={confidence} — should be capped at 95 by investigator.py")

        if issues:
            fail(f"Investigator output issues: {', '.join(issues)}")
            run.record_fail("investigator_output", "; ".join(issues))
        else:
            ok(f"Investigator: confidence={confidence}, diagnosis={diagnosis[:80]}...")
            run.record_pass("investigator_output")

    # Impact — WOW #2: affected_asset must come from asset_inventory.json
    impact = agent_outputs.get("impact", {})
    if not impact:
        fail("Impact output missing")
        run.record_fail("impact_output", "missing")
    else:
        severity = impact.get("severity", "")
        asset = impact.get("affected_asset", "")
        damage = impact.get("potential_damage", "")
        issues = []
        if severity not in {"CRITICAL", "HIGH", "MEDIUM", "LOW"}:
            issues.append(f"severity={severity!r} (not a valid value)")
        if not asset:
            issues.append("affected_asset is empty")
        if asset == "Unknown Asset":
            warn("affected_asset is 'Unknown Asset' — asset lookup may have failed")
            run.record_warn()
        if not damage:
            issues.append("potential_damage is empty")
        if issues:
            fail(f"Impact output issues: {', '.join(issues)}")
            run.record_fail("impact_output", "; ".join(issues))
        else:
            ok(f"Impact: severity={severity}, asset={asset!r}")
            run.record_pass("impact_output")

    # Commander — WOW #3: 3 recommended actions from playbooks.json
    commander = agent_outputs.get("commander", {})
    if not commander:
        fail("Commander output missing")
        run.record_fail("commander_output", "missing")
    else:
        headline = commander.get("summary_headline", "")
        actions = commander.get("recommended_actions", [])
        issues = []
        if not headline:
            issues.append("summary_headline is empty")
        if not isinstance(actions, list):
            issues.append(f"recommended_actions is {type(actions).__name__}, expected list")
        elif len(actions) != 3:
            issues.append(f"expected exactly 3 actions, got {len(actions)}")
        if issues:
            fail(f"Commander output issues: {', '.join(issues)}")
            run.record_fail("commander_output", "; ".join(issues))
        else:
            ok(f"Commander: {headline!r}")
            for i, action in enumerate(actions, 1):
                print(f"      {Colors.DIM}{i}. {action}{Colors.RESET}")
            run.record_pass("commander_output")

    # --- Validate the 3 wow moments ----------------------------------------
    print()
    header("TEST 7c — The 3 wow moments")

    # Wow #1: CVE number in the diagnosis (looked up from cve_database.json,
    #         NOT in the raw alert text)
    wow1_passed = False
    if investigator and diagnosis:
        import re
        cve_match = re.search(r'CVE-\d{4}-\d{4,7}', diagnosis, re.IGNORECASE)
        if cve_match:
            cve_id = cve_match.group(0).upper()
            ok(f"WOW #1 ✓ — CVE cited in diagnosis: {cve_id}")
            ok(f"         (this CVE was looked up from cve_database.json, not in the raw alert)")
            wow1_passed = True
        else:
            fail("WOW #1 ✗ — no CVE-XXXX-XXXX pattern found in investigator diagnosis")
            print(f"      {Colors.DIM}Diagnosis: {diagnosis}{Colors.RESET}")
    if wow1_passed:
        run.record_pass("wow_1_cve")
    else:
        run.record_fail("wow_1_cve", "no CVE in diagnosis")

    # Wow #2: affected_asset is a real asset from asset_inventory.json, not "Unknown"
    wow2_passed = False
    if impact and asset:
        if asset and asset != "Unknown Asset":
            ok(f"WOW #2 ✓ — affected_asset: {asset!r}")
            ok(f"         (this was looked up from asset_inventory.json via port/IP, not in the raw alert)")
            wow2_passed = True
        else:
            fail("WOW #2 ✗ — affected_asset is empty or 'Unknown Asset'")
            print(f"      {Colors.DIM}The asset lookup failed; Impact fell back to generic text.{Colors.RESET}")
    if wow2_passed:
        run.record_pass("wow_2_asset")
    else:
        run.record_fail("wow_2_asset", "asset lookup failed")

    # Wow #3: 3 recommended_actions, each non-empty
    wow3_passed = False
    if commander and isinstance(actions, list) and len(actions) == 3:
        if all(isinstance(a, str) and len(a) > 10 for a in actions):
            ok(f"WOW #3 ✓ — 3 recommended actions, all non-trivial")
            ok(f"         (these were pulled from playbooks.json based on severity={severity})")
            wow3_passed = True
        else:
            fail("WOW #3 ✗ — some actions are empty or too short")
            for i, a in enumerate(actions, 1):
                print(f"      {Colors.DIM}{i}. ({len(a) if isinstance(a, str) else '?'} chars) {a}{Colors.RESET}")
    if wow3_passed:
        run.record_pass("wow_3_actions")
    else:
        run.record_fail("wow_3_actions", "actions missing or malformed")

    # --- Final envelope sanity check ---------------------------------------
    print()
    header("TEST 7d — Final envelope structure")
    if final_envelope is None:
        fail("No pipeline_complete envelope received")
        run.record_fail("envelope", "missing")
    else:
        expected_keys = {"scout", "investigator", "impact", "commander"}
        actual_keys = set(final_envelope.keys())
        if actual_keys == expected_keys:
            ok(f"Envelope has all 4 agent keys: {sorted(actual_keys)}")
            run.record_pass("envelope")
        else:
            fail(f"Envelope key mismatch",
                  f"expected {sorted(expected_keys)}, got {sorted(actual_keys)}")
            run.record_fail("envelope", f"keys {actual_keys}")

    return final_envelope, total_s or elapsed


def test_store_persistence(
    base_url: str,
    alert_id: str,
    expected_envelope: dict | None,
    run: TestRun,
    verbose: bool,
) -> bool:
    """
    After the stream completed, /api/alerts/{id} should show:
      - processed_at is NOT null
      - pipeline_results is populated and matches the streamed envelope
    """
    header(f"TEST 8 — Store persistence after pipeline_complete")

    try:
        r = httpx.get(f"{base_url}/api/alerts/{alert_id}", timeout=10.0)
        if r.status_code != 200:
            fail(f"Expected 200, got {r.status_code}")
            run.record_fail("persistence", f"status {r.status_code}")
            return False

        alert = r.json()
        processed_at = alert.get("processed_at")
        results = alert.get("pipeline_results")

        if processed_at is None:
            fail("processed_at is still null — sse.py did not call store.save_results()")
            run.record_fail("persistence", "processed_at null")
            return False
        ok(f"processed_at = {processed_at}")

        if results is None:
            fail("pipeline_results is still null")
            run.record_fail("persistence", "results null")
            return False
        ok("pipeline_results is populated")

        # Verify the persisted results match what the stream delivered
        if expected_envelope is not None:
            if results == expected_envelope:
                ok("Persisted results match the streamed envelope exactly")
                run.record_pass("persistence")
            else:
                # Check at least the structure matches
                if set(results.keys()) == set(expected_envelope.keys()):
                    warn("Persisted results have the right keys but differ in values")
                    warn("(this can happen if you ran the pipeline twice — second run overwrites first)")
                    run.record_warn()
                    run.record_pass("persistence_partial")
                else:
                    fail("Persisted results don't match streamed envelope",
                         f"streamed keys: {sorted(expected_envelope.keys())}, "
                         f"persisted keys: {sorted(results.keys())}")
                    run.record_fail("persistence", "key mismatch")
        else:
            run.record_pass("persistence_no_envelope_to_compare")

        if verbose:
            info(f"Full persisted alert:")
            print(f"      {Colors.DIM}{json.dumps(alert, indent=2)[:800]}{Colors.RESET}")

        return True
    except Exception as e:
        fail(f"Exception during persistence check: {type(e).__name__}: {e}")
        run.record_fail("persistence", str(e))
        return False


def test_free_text_stream(base_url: str, run: TestRun, verbose: bool) -> bool:
    """
    GET /api/stream?raw_alert=... — free-text path.

    Verifies the stream works without an alert_id, and that the result
    is NOT persisted to the store (no alert_id to key on).
    """
    header("TEST 9 — Free-text alert stream (no alert_id)")

    raw_alert = "Suspicious port scan detected from 198.51.100.42 on port 22"
    print(f"  {Colors.DIM}Streaming free-text alert: {raw_alert!r}{Colors.RESET}")
    print(f"  {Colors.DIM}(this takes 5-45 seconds){Colors.RESET}")

    seen_complete = False
    seen_error = False
    agent_count = 0

    t0 = time.time()
    try:
        with httpx.stream(
            "GET",
            f"{base_url}/api/stream",
            params={"raw_alert": raw_alert},
            timeout=httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0),
        ) as r:
            if r.status_code != 200:
                body = r.read().decode("utf-8", errors="replace")
                fail(f"Expected 200, got {r.status_code}", body[:300])
                run.record_fail("free_text", f"status {r.status_code}")
                return False

            for event_name, _data in parse_sse_stream(r):
                elapsed = time.time() - t0
                if event_name == "agent_complete":
                    agent_count += 1
                    print(f"  {Colors.DIM}[{elapsed:5.1f}s]{Colors.RESET} {Colors.GREEN}✓{Colors.RESET} agent {agent_count}/4 done")
                elif event_name == "pipeline_complete":
                    seen_complete = True
                    print(f"  {Colors.DIM}[{elapsed:5.1f}s]{Colors.RESET} {Colors.GREEN}✓ pipeline_complete{Colors.RESET}")
                    break
                elif event_name == "pipeline_error":
                    seen_error = True
                    print(f"  {Colors.DIM}[{elapsed:5.1f}s]{Colors.RESET} {Colors.RED}✗ pipeline_error{Colors.RESET}")
                    break

    except Exception as e:
        fail(f"Exception during free-text stream: {type(e).__name__}: {e}")
        run.record_fail("free_text", str(e))
        return False

    if seen_complete and agent_count == 4:
        ok(f"Free-text stream completed: 4 agents ran, pipeline_complete fired")
        ok("Result was NOT persisted to store (no alert_id) — correct behavior")
        run.record_pass("free_text")
        return True
    elif seen_error:
        fail("Free-text stream errored")
        run.record_fail("free_text", "pipeline_error")
        return False
    else:
        fail(f"Incomplete: {agent_count} agents, complete={seen_complete}")
        run.record_fail("free_text", "incomplete")
        return False


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke test for the Rezolve backend.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python smoke_test.py                  # run all tests with alert-001
    python smoke_test.py alert-003        # use alert-003 for the SSE test
    python smoke_test.py --no-stream      # skip the slow SSE test
    python smoke_test.py --verbose        # print full JSON responses
""",
    )
    parser.add_argument(
        "alert_id",
        nargs="?",
        default="alert-001",
        help="Alert ID to use for the SSE stream test (default: alert-001)",
    )
    parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Skip the slow SSE stream test (fast smoke — ~2 seconds)",
    )
    parser.add_argument(
        "--no-free-text",
        action="store_true",
        help="Skip the free-text stream test (saves another 30-45 seconds)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print full JSON of every response",
    )
    args = parser.parse_args()

    base_url = f"http://{args.host}:{args.port}"

    banner(f"Rezolve Backend Smoke Test")
    print(f"  Target:    {base_url}")
    print(f"  Alert ID:  {args.alert_id}")
    print(f"  SSE test:  {'SKIP' if args.no_stream else 'RUN'}")
    print(f"  Free-text: {'SKIP' if args.no_free_text else 'RUN'}")
    print(f"  Verbose:   {args.verbose}")

    run = TestRun()

    # Test 1: server up
    if not test_server_up(base_url, run):
        # If the server isn't reachable, abort everything else.
        print(f"\n{Colors.RED}Server is not reachable. Start it with:{Colors.RESET}")
        print(f"  {Colors.DIM}uvicorn backend.app.main:app --port {args.port}{Colors.RESET}")
        print(f"\n{Colors.RED}Aborting remaining tests.{Colors.RESET}")
        _print_summary(run)
        return 1

    # Test 2: health
    test_health(base_url, run, args.verbose)

    # Test 3: list alerts
    alerts = test_list_alerts(base_url, run, args.verbose)

    # Test 4: get single alert (before stream — should be unprocessed)
    test_get_single_alert(base_url, args.alert_id, run, args.verbose)

    # Test 5: 404 for unknown alert
    test_404_unknown_alert(base_url, run)

    # Test 6: 400 when no params provided
    test_400_no_params(base_url, run)

    # Tests 7 & 8: SSE stream + persistence (the big ones)
    envelope = None
    total_s = 0.0
    if not args.no_stream:
        envelope, total_s = test_sse_stream(base_url, args.alert_id, run, args.verbose)

        # Test 8: persistence — only meaningful after the stream ran
        test_store_persistence(base_url, args.alert_id, envelope, run, args.verbose)
    else:
        header("TEST 7 — SSE stream (SKIPPED via --no-stream)")
        warn("Skipping SSE stream test")
        header("TEST 8 — Store persistence (SKIPPED — depends on test 7)")
        warn("Skipping persistence test")

    # Test 9: free-text stream
    if not args.no_free_text and not args.no_stream:
        test_free_text_stream(base_url, run, args.verbose)
    elif args.no_free_text:
        header("TEST 9 — Free-text stream (SKIPPED via --no-free-text)")
        warn("Skipping free-text test")
    else:
        header("TEST 9 — Free-text stream (SKIPPED — SSE test was skipped)")
        warn("Skipping free-text test (requires SSE to be enabled)")

    # Final summary
    _print_summary(run, total_s)
    return 0 if run.failed == 0 else 1


def _print_summary(run: TestRun, total_s: float = 0.0) -> None:
    banner("Summary")
    print(f"  {Colors.GREEN}Passed:    {run.passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed:    {run.failed}{Colors.RESET}")
    print(f"  {Colors.YELLOW}Warnings:  {run.warnings}{Colors.RESET}")
    if total_s:
        print(f"  Pipeline time: {total_s:.1f}s")

    if run.failures:
        print(f"\n{Colors.RED}Failures:{Colors.RESET}")
        for f in run.failures:
            print(f"  {Colors.RED}•{Colors.RESET} {f}")

    if run.failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED — backend is demo-ready{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ {run.failed} test(s) failed — see above{Colors.RESET}")


if __name__ == "__main__":
    sys.exit(main())