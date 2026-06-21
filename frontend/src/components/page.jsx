import React, { useEffect } from "react";
import RawLogFeed from "./RawLogFeed";
import AgentPipeline from "./AgentPipeline";
import ExecutiveBrief from "./ExecutiveBrief";
import Header from "./Header";
import Footer from "./Footer";
import { AnimatePresence, motion } from "framer-motion";
import { useSSEPipeline } from "../hooks/useSSEPipeline";
import { RefreshCw, Loader2, AlertTriangle } from "lucide-react";

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

  useEffect(() => {
    run("alert-001");
  }, []);

  const pipelineStep = derivePipelineStep(agentStates);

  const isRunning = status === "running";
  const isComplete = status === "complete";
  const hasStarted = status !== "idle";

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col">
      {/* SAME HEADER AS LANDING PAGE */}
      <Header />

      {/* Top Status Bar */}
      <div className="mt-20 shrink-0 flex items-center justify-between px-4 py-2 bg-white border-b border-slate-200 shadow-sm">
        <div className="flex items-center gap-2">
          <span className="font-mono text-xs font-bold text-slate-500 uppercase tracking-widest">
            reZolve · Decision Pipeline
          </span>

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

        <button
          onClick={() => run("alert-001")}
          disabled={isRunning}
          className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-900 text-white hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          <RefreshCw className={`w-3 h-3 ${isRunning ? "animate-spin" : ""}`} />
          Run Again
        </button>
      </div>

      {/* Error Banner */}
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

      {/* SAME FOOTER AS LANDING PAGE */}
      <Footer />
    </div>
  );
}
