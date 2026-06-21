/**
 * useSSEPipeline.js
 *
 * Custom React hook that opens an EventSource to /api/stream?alert_id=<id>
 * and converts the SSE event stream into React state that drives the demo UI.
 *
 * State shape:
 *   status      : "idle" | "running" | "complete" | "error"
 *   rawAlert    : string — the raw_alert text from pipeline_start
 *   agentStates : { scout, investigator, impact, commander }
 *                 each entry is null | { status: "running"|"done", output, elapsed_s }
 *   results     : null | PipelineResults envelope from pipeline_complete
 *   error       : null | string
 *
 * Usage:
 *   const { status, rawAlert, agentStates, results, error, run } = useSSEPipeline();
 *   run("alert-001");   // start / restart
 */
import { useState, useRef, useCallback } from "react";

const AGENTS = ["scout", "investigator", "impact", "commander"];

function freshAgentStates() {
  return Object.fromEntries(AGENTS.map((a) => [a, null]));
}

export function useSSEPipeline() {
  const [status, setStatus] = useState("idle");
  const [rawAlert, setRawAlert] = useState(null);
  const [agentStates, setAgentStates] = useState(freshAgentStates);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Keep a ref to the open EventSource so we can close it on re-run / unmount
  const esRef = useRef(null);

  const run = useCallback((alertId = "alert-001") => {
    // Close any existing stream before opening a new one
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
    }

    // Reset all state
    setStatus("running");
    setRawAlert(null);
    setAgentStates(freshAgentStates());
    setResults(null);
    setError(null);

    const url = `/api/stream?alert_id=${encodeURIComponent(alertId)}`;
    const es = new EventSource(url);
    esRef.current = es;

    // ── pipeline_start ────────────────────────────────────────────────────────
    es.addEventListener("pipeline_start", (e) => {
      const data = JSON.parse(e.data);
      setRawAlert(data.raw_alert);
    });

    // ── agent_start ───────────────────────────────────────────────────────────
    es.addEventListener("agent_start", (e) => {
      const { agent } = JSON.parse(e.data);
      setAgentStates((prev) => ({
        ...prev,
        [agent]: { status: "running", output: null, elapsed_s: null },
      }));
    });

    // ── agent_complete ────────────────────────────────────────────────────────
    es.addEventListener("agent_complete", (e) => {
      const { agent, output, elapsed_s } = JSON.parse(e.data);
      setAgentStates((prev) => ({
        ...prev,
        [agent]: { status: "done", output, elapsed_s },
      }));
    });

    // ── pipeline_complete ─────────────────────────────────────────────────────
    es.addEventListener("pipeline_complete", (e) => {
      const { results: envelope } = JSON.parse(e.data);
      setResults(envelope);
      setStatus("complete");
      es.close();
      esRef.current = null;
    });

    // ── pipeline_error ────────────────────────────────────────────────────────
    es.addEventListener("pipeline_error", (e) => {
      const { message } = JSON.parse(e.data);
      setError(message);
      setStatus("error");
      es.close();
      esRef.current = null;
    });

    // Network-level error (server down, CORS, etc.)
    es.onerror = () => {
      setError("Connection to backend lost. Is the server running on :8000?");
      setStatus("error");
      es.close();
      esRef.current = null;
    };
  }, []);

  return { status, rawAlert, agentStates, results, error, run };
}
