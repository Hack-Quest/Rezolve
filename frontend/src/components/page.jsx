import React, { useState, useEffect } from "react";
import RawLogFeed from "./RawLogFeed";
import AgentPipeline from "./AgentPipeline";
import ExecutiveBrief from "./ExecutiveBrief";
import Header from "./Header";
import Footer from "./Footer";
import { AnimatePresence, motion } from "framer-motion";
import { useSSEPipeline } from "../hooks/useSSEPipeline";
import {
  RefreshCw,
  Loader2,
  AlertTriangle,
  Shuffle,
  ChevronDown,
} from "lucide-react";

function derivePipelineStep(agentStates) {
  const order = ["scout", "investigator", "impact", "commander"];
  let step = 0;
  for (const name of order) {
    if (agentStates[name]?.status === "done") {
      step++;
    } else {
      break;
    }
  }
  return step;
}

export default function Page() {
  const { status, rawAlert, agentStates, results, error, run } =
    useSSEPipeline();

  const [alerts, setAlerts] = useState([]);
  const [alertsLoading, setAlertsLoading] = useState(true);
  const [alertsError, setAlertsError] = useState(null);
  const [selectedAlertId, setSelectedAlertId] = useState(null);
  const [showAlertList, setShowAlertList] = useState(false);

  // Fetch the alert list once on mount, then pick a random one and auto-run it
  useEffect(() => {
    let cancelled = false;
    setAlertsLoading(true);
    setAlertsError(null);

    fetch("/api/alerts")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (cancelled) return;
        if (!Array.isArray(data) || data.length === 0) {
          throw new Error("No alerts returned by backend");
        }
        setAlerts(data);
        setAlertsLoading(false);
        const randomAlert = data[Math.floor(Math.random() * data.length)];
        setSelectedAlertId(randomAlert.id);
        run(randomAlert.id);
      })
      .catch((err) => {
        if (cancelled) return;
        console.error("Failed to load alerts:", err);
        setAlertsError(
          `Could not reach backend at /api/alerts. Is uvicorn running on :8000? (${err.message})`
        );
        setAlertsLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // run is stable (useCallback with [] in the hook), so this runs once
  }, [run]);

  const pipelineStep = derivePipelineStep(agentStates);
  const isRunning = status === "running";
  const isComplete = status === "complete";
  const hasStarted = status !== "idle";

  const currentAlert = alerts.find((a) => a.id === selectedAlertId);

  // Pick a random alert (different from current if possible) and run it
  const handleRunRandom = () => {
    if (alerts.length === 0) return;
    let pool = alerts;
    if (alerts.length > 1 && selectedAlertId) {
      pool = alerts.filter((a) => a.id !== selectedAlertId);
    }
    const randomAlert = pool[Math.floor(Math.random() * pool.length)];
    setSelectedAlertId(randomAlert.id);
    setShowAlertList(false);
    run(randomAlert.id);
  };

  // Run a specific alert chosen from the dropdown
  const handleSelectAlert = (alertId) => {
    setSelectedAlertId(alertId);
    setShowAlertList(false);
    run(alertId);
  };

  // Re-run the currently selected alert
  const handleRunAgain = () => {
    if (selectedAlertId) run(selectedAlertId);
  };

  const severityBadgeClass = (sev) =>
    sev === "CRITICAL"
      ? "bg-rose-100 text-rose-700"
      : sev === "HIGH"
        ? "bg-orange-100 text-orange-700"
        : sev === "MEDIUM"
          ? "bg-amber-100 text-amber-700"
          : "bg-emerald-100 text-emerald-700";

  // Show a full-screen error if we can't even load the alert list
  if (alertsError && alerts.length === 0) {
    return (
      <div className="min-h-screen bg-slate-100 flex flex-col">
        <Header />
        <div className="mt-20 flex-1 flex items-center justify-center p-8">
          <div className="bg-white border border-rose-200 rounded-xl p-8 max-w-md text-center shadow-sm">
            <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto mb-4" />
            <h2 className="text-lg font-bold text-slate-900 mb-2">
              Backend unreachable
            </h2>
            <p className="text-sm text-slate-600 font-mono mb-4">
              {alertsError}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-slate-700 transition-all"
            >
              Retry
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Brief loading state while fetching the alert list on first mount
  if (alertsLoading) {
    return (
      <div className="min-h-screen bg-slate-100 flex flex-col">
        <Header />
        <div className="mt-20 flex-1 flex items-center justify-center">
          <div className="flex items-center gap-2 text-slate-500 font-mono text-sm">
            <Loader2 className="w-4 h-4 animate-spin" />
            Loading alerts…
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col">
      <Header />

      {/* Top Status Bar */}
      <div className="mt-20 shrink-0 flex items-center justify-between px-4 py-2 bg-white border-b border-slate-200 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="font-mono text-xs font-bold text-slate-500 uppercase tracking-widest">
            reZolve · Decision Pipeline
          </span>

          {currentAlert && (
            <span className="flex items-center gap-1.5 text-[10px] font-mono text-slate-400">
              · {currentAlert.id}
              <span
                className={`px-1.5 py-0.5 rounded font-bold ${severityBadgeClass(
                  currentAlert.severity
                )}`}
              >
                {currentAlert.severity}
              </span>
            </span>
          )}

          {isRunning && (
            <span className="flex items-center gap-1 text-[10px] font-mono text-amber-600 bg-amber-50 px-2 py-0.5 rounded border border-amber-100 animate-pulse">
              <Loader2 className="w-2.5 h-2.5 animate-spin" />
              Running...
            </span>
          )}

          {isComplete && (
            <span className="text-[10px] font-mono text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100">
              ✓ Complete
            </span>
          )}

          {status === "error" && (
            <span className="flex items-center gap-1 text-[10px] font-mono text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-100">
              <AlertTriangle className="w-2.5 h-2.5" />
              Error
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {/* Alert Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowAlertList((v) => !v)}
              disabled={isRunning || alertsLoading}
              className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all max-w-[220px]"
              title={currentAlert ? currentAlert.title : "Select alert"}
            >
              <span className="truncate">
                {alertsLoading
                  ? "Loading alerts..."
                  : currentAlert
                    ? currentAlert.title
                    : "Select alert"}
              </span>
              <ChevronDown className="w-3 h-3 shrink-0" />
            </button>

            {showAlertList && (
              <>
                {/* Click-away overlay */}
                <div
                  className="fixed inset-0 z-40"
                  onClick={() => setShowAlertList(false)}
                />
                {/* Dropdown panel */}
                <div className="absolute right-0 mt-1 w-80 max-h-96 overflow-y-auto bg-white border border-slate-200 rounded-lg shadow-xl z-50">
                  {alerts.map((alert) => (
                    <button
                      key={alert.id}
                      onClick={() => handleSelectAlert(alert.id)}
                      className={`w-full text-left px-3 py-2 hover:bg-slate-50 border-b border-slate-100 last:border-b-0 transition-colors ${
                        alert.id === selectedAlertId ? "bg-rose-50" : ""
                      }`}
                    >
                      <div className="flex items-center justify-between mb-0.5">
                        <span className="text-[10px] font-mono text-slate-400">
                          {alert.id}
                        </span>
                        <span
                          className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ${severityBadgeClass(
                            alert.severity
                          )}`}
                        >
                          {alert.severity}
                        </span>
                      </div>
                      <div className="text-xs font-semibold text-slate-800 truncate">
                        {alert.title}
                      </div>
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Random button */}
          <button
            onClick={handleRunRandom}
            disabled={isRunning || alertsLoading || alerts.length === 0}
            className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-rose-600 text-white hover:bg-rose-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            title="Pick a random alert and run it"
          >
            <Shuffle className="w-3 h-3" />
            Random
          </button>

          {/* Run Again button */}
          <button
            onClick={handleRunAgain}
            disabled={isRunning || !selectedAlertId || alertsLoading}
            className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-900 text-white hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            <RefreshCw
              className={`w-3 h-3 ${isRunning ? "animate-spin" : ""}`}
            />
            Run Again
          </button>
        </div>
      </div>

      {/* Error Banner (for pipeline errors, not fetch errors) */}
      {error && (
        <div className="shrink-0 flex items-center gap-2 px-4 py-2 bg-rose-50 border-b border-rose-200 text-rose-700 text-xs font-mono">
          <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
          {error}
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 px-4 py-4 min-h-0">
        <div className="grid grid-cols-12 gap-4 h-full">
          {/* Raw Logs */}
          <RawLogFeed rawAlert={rawAlert} />

          {/* Agent Pipeline */}
          <AnimatePresence mode="wait">
            {hasStarted && (
              <motion.div
                key="agent-pipeline-wrapper"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
                className="col-span-5 h-full flex flex-col min-h-0"
              >
                <AgentPipeline
                  pipelineStep={pipelineStep}
                  agentStates={agentStates}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Executive Brief */}
          <AnimatePresence mode="wait">
            {isComplete && results && (
              <motion.div
                key="executive-brief-wrapper"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{
                  type: "spring",
                  stiffness: 100,
                  damping: 15,
                }}
                className="col-span-4 h-full flex flex-col min-h-0"
              >
                <ExecutiveBrief results={results} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      <Footer />
    </div>
  );
}