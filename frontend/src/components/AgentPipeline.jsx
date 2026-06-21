import React from "react";
import { Search, Microscope, Zap, SquareTerminal, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

/**
 * AgentPipeline
 *
 * Props:
 *   pipelineStep : number (0–4) — used for the vertical progress line animation
 *   agentStates  : { scout, investigator, impact, commander }
 *                  each entry: null | { status: "running"|"done", output, elapsed_s }
 */
export default function AgentPipeline({ pipelineStep, agentStates = {} }) {
  // Build a data-row array for each agent from the live SSE output.
  // Falls back to placeholder dashes while the agent hasn't run yet.
  function scoutRows(output) {
    if (!output) return [
      { label: "Target", val: "—" },
      { label: "Attacker IP", val: "—" },
      { label: "Action", val: "—" },
    ];
    return [
      { label: "Target", val: output.target },
      { label: "Attacker IP", val: output.attacker_ip },
      { label: "Action", val: output.action },
    ];
  }

  function investigatorRows(output) {
    if (!output) return [
      { label: "Diagnosis", val: "—" },
      { label: "Confidence", val: "—" },
    ];
    return [
      { label: "Diagnosis", val: output.diagnosis },
      { label: "Confidence", val: `${output.confidence_score}%`, highlightVal: output.confidence_score >= 80 },
    ];
  }

  function impactRows(output) {
    if (!output) return [
      { label: "Severity", val: "—" },
      { label: "Asset", val: "—" },
      { label: "Damage", val: "—" },
    ];
    return [
      { label: "Severity", val: output.severity, highlightVal: true },
      { label: "Asset", val: output.affected_asset, boldVal: true },
      { label: "Damage", val: output.potential_damage },
    ];
  }

  function commanderRows(output) {
    if (!output) return [
      { label: "Headline", val: "—" },
      { label: "Actions", val: "—" },
    ];
    return [
      { label: "Headline", val: output.summary_headline },
      { label: "Actions", val: `${(output.recommended_actions || []).length} steps` },
    ];
  }

  const agents = [
    {
      index: 1,
      key: "scout",
      name: "Scout",
      desc: "picks out the key facts",
      icon: Search,
      colorClass: "bg-slate-800",
      highlight: false,
      rows: scoutRows,
    },
    {
      index: 2,
      key: "investigator",
      name: "Investigator",
      desc: "names the vulnerability",
      icon: Microscope,
      colorClass: "bg-slate-800",
      highlight: false,
      rows: investigatorRows,
    },
    {
      index: 3,
      key: "impact",
      name: "Impact",
      desc: "finds what's actually at risk",
      icon: Zap,
      colorClass: "bg-rose-600",
      highlight: true,
      rows: impactRows,
    },
    {
      index: 4,
      key: "commander",
      name: "Commander",
      desc: "writes the action plan",
      icon: SquareTerminal,
      colorClass: "bg-slate-800",
      highlight: false,
      rows: commanderRows,
    },
  ];

  const cardVariants = {
    incomplete: {
      opacity: 0.5,
      scale: 1,
      transition: { duration: 0.3 },
    },
    completed: {
      opacity: 1,
      scale: [1, 1.05, 1],
      transition: {
        opacity: { duration: 0.4 },
        scale: { duration: 0.4, times: [0, 0.5, 1] },
      },
    },
  };

  return (
    <div className="col-span-5 h-full flex flex-col min-h-0 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden select-none">
      {/* Header */}
      <div className="shrink-0 p-3 border-b border-slate-100 font-bold text-slate-800 uppercase tracking-wider text-xs flex justify-between items-center">
        <span>02 // THE FOUR AI AGENTS</span>
        <span className="material-symbols-outlined text-slate-400 text-[16px]">
          memory
        </span>
      </div>

      {/* Pipeline cards */}
      <div className="flex-1 overflow-y-auto min-h-0 p-4 space-y-3 relative">
        {/* Vertical connecting line */}
        <div className="absolute left-[36px] top-[40px] bottom-[40px] w-px bg-slate-200 z-0">
          <motion.div
            className="absolute top-0 left-0 w-full bg-gradient-to-b from-slate-800 via-rose-500 to-rose-600 origin-top"
            initial={{ height: "0%" }}
            animate={{
              height:
                pipelineStep === 0
                  ? "0%"
                  : pipelineStep === 1
                    ? "15%"
                    : pipelineStep === 2
                      ? "48%"
                      : pipelineStep === 3
                        ? "80%"
                        : "100%",
            }}
            transition={{ duration: 0.8, ease: "easeInOut" }}
          />
        </div>

        {agents.map((agent) => {
          const state = agentStates[agent.key] || null;
          const isCompleted = state?.status === "done";
          const isProcessing = state?.status === "running";
          const AgentIcon = agent.icon;
          const dataRows = agent.rows(state?.output ?? null);

          return (
            <motion.div
              key={agent.index}
              variants={cardVariants}
              initial="incomplete"
              animate={isCompleted ? "completed" : "incomplete"}
              className="flex gap-3 group relative z-10"
            >
              {/* Avatar Ring */}
              <div
                className={`flex-none w-8 h-8 rounded-full border-4 border-white flex items-center justify-center shadow-sm transition-all duration-300 ${
                  isCompleted ? agent.colorClass : isProcessing ? "bg-amber-400" : "bg-slate-300"
                } ${isCompleted && agent.highlight ? "ring-2 ring-rose-100" : ""}`}
              >
                {isProcessing ? (
                  <Loader2 className="w-3.5 h-3.5 text-white animate-spin" />
                ) : (
                  <AgentIcon className="w-3.5 h-3.5 text-white" />
                )}
              </div>

              {/* Card Body */}
              <div
                className={`flex-grow border rounded-lg p-2.5 transition-all duration-300 ${
                  isCompleted
                    ? agent.highlight
                      ? "bg-rose-50 border-rose-200 shadow-sm"
                      : "bg-slate-50 border-slate-200"
                    : "bg-white border-slate-100 opacity-60"
                }`}
              >
                <div className="flex justify-between items-center mb-1.5">
                  <h3
                    className={`text-sm font-semibold transition-colors duration-300 ${
                      isCompleted && agent.highlight
                        ? "text-rose-900"
                        : "text-slate-900"
                    }`}
                  >
                    {agent.name}{" "}
                    <span
                      className={`text-xs font-normal transition-colors duration-300 ${
                        isCompleted && agent.highlight
                          ? "text-rose-600/70"
                          : "text-slate-500"
                      }`}
                    >
                      · {agent.desc}
                    </span>
                  </h3>

                  {/* Status badge */}
                  {isCompleted ? (
                    <span
                      className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                        agent.highlight
                          ? "text-rose-600 bg-white border-rose-200"
                          : "text-emerald-600 bg-emerald-50 border-emerald-100"
                      }`}
                    >
                      ✓ {state?.elapsed_s != null ? `${state.elapsed_s}s` : "done"}
                    </span>
                  ) : isProcessing ? (
                    <span className="flex items-center gap-1 text-[10px] font-mono text-amber-600 bg-amber-50 px-2 py-0.5 rounded border border-amber-100 animate-pulse">
                      <Loader2 className="w-2.5 h-2.5 animate-spin" />
                      Running…
                    </span>
                  ) : (
                    <span className="text-[10px] font-mono text-slate-400 bg-slate-50 px-2 py-0.5 rounded border border-slate-100">
                      Pending
                    </span>
                  )}
                </div>

                {/* Data grid */}
                <div
                  className={`grid grid-cols-[90px_1fr] gap-x-2 gap-y-1 text-[10px] pt-1.5 border-t mt-1.5 transition-colors duration-300 ${
                    agent.highlight ? "border-rose-200" : "border-slate-200"
                  }`}
                >
                  {dataRows.map((row, idx) => (
                    <React.Fragment key={idx}>
                      <span
                        className={`font-medium transition-colors duration-300 ${
                          agent.highlight
                            ? "text-rose-700/60"
                            : "text-slate-400"
                        }`}
                      >
                        {row.label}
                      </span>
                      <span
                        className={`font-mono transition-colors duration-300 ${
                          row.highlightVal
                            ? "text-rose-600 font-bold"
                            : row.boldVal
                              ? "text-slate-900 font-bold"
                              : "text-slate-700"
                        }`}
                      >
                        {row.val}
                      </span>
                    </React.Fragment>
                  ))}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
