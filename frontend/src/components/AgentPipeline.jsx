import React from "react";
import { Search, Microscope, Zap, SquareTerminal, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

export default function AgentPipeline({ pipelineStep }) {
  // Define agent card details
  const agents = [
    {
      index: 1,
      name: "Scout",
      desc: "picks out the key facts",
      icon: Search,
      time: "1.2s",
      colorClass: "bg-slate-800",
      highlight: false,
      data: [
        { label: "Source IP", val: "198.51.100.42" },
        { label: "Port", val: "8080" },
        { label: "Framework", val: "Apache Struts" },
        { label: "Action", val: "unauthorized_db_access" },
      ],
    },
    {
      index: 2,
      name: "Investigator",
      desc: "names the vulnerability",
      icon: Microscope,
      time: "3.1s",
      colorClass: "bg-slate-800",
      highlight: false,
      data: [
        { label: "CVE", val: "CVE-2017-5638" },
        { label: "CVSS", val: "9.8 · Critical", highlightVal: true },
        { label: "Attack type", val: "remote code execution" },
        { label: "Confidence", val: "0.92" },
      ],
    },
    {
      index: 3,
      name: "Impact",
      desc: "finds what's actually at risk",
      icon: Zap,
      time: "4.8s",
      colorClass: "bg-rose-600",
      highlight: true,
      data: [
        { label: "Asset ID", val: "AST-PAY-0042" },
        { label: "Asset", val: "Production Struts Gateway", boldVal: true },
        { label: "Segment", val: "Payments Gateway" },
        { label: "Records", val: "5,247,891", boldVal: true },
      ],
    },
    {
      index: 4,
      name: "Commander",
      desc: "writes the action plan",
      icon: SquareTerminal,
      time: "2.7s",
      colorClass: "bg-slate-800",
      highlight: false,
      data: [
        { label: "Severity", val: "Critical" },
        { label: "Actions", val: "3 prioritized" },
        { label: "Posture", val: "isolate · escalate · remediate" },
      ],
    },
  ];

  // Define card variants for Framer Motion pop animation
  const cardVariants = {
    incomplete: {
      opacity: 0.5,
      scale: 1,
      y: 0,
      transition: { duration: 0.3 },
    },
    completed: {
      opacity: 1,
      scale: [1, 1.05, 1],
      y: 0,
      transition: {
        opacity: { duration: 0.4 },
        scale: { duration: 0.4, times: [0, 0.5, 1] },
        y: { duration: 0.4 },
      },
    },
  };

  return (
    <div className="col-span-5 h-full flex flex-col min-h-0 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden select-none">
      {/* Header block */}
      <div className="shrink-0 p-3 border-b border-slate-100 font-bold text-slate-800 uppercase tracking-wider text-xs flex justify-between items-center">
        <span>02 // THE FOUR AI AGENTS</span>
        <span className="material-symbols-outlined text-slate-400 text-[16px]">
          memory
        </span>
      </div>

      {/* Agents pipeline container */}
      <div className="flex-1 overflow-y-auto min-h-0 p-4 space-y-3 relative">
        {/* Dynamic Vertical Connecting Line */}
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

        {/* Agent Cards */}
        {agents.map((agent) => {
          const isCompleted = pipelineStep >= agent.index;
          const isProcessing = pipelineStep === agent.index - 1;
          const AgentIcon = agent.icon;

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
                  isCompleted ? agent.colorClass : "bg-slate-300"
                } ${isCompleted && agent.highlight ? "ring-2 ring-rose-100" : ""}`}
              >
                {isProcessing ? (
                  <Loader2 className="w-3.5 h-3.5 text-slate-500 animate-spin" />
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

                  {/* Status Badge */}
                  {isCompleted ? (
                    <span
                      className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                        agent.highlight
                          ? "text-rose-600 bg-white border-rose-200"
                          : "text-emerald-600 bg-emerald-50 border-emerald-100"
                      }`}
                    >
                      ✓ {agent.time}
                    </span>
                  ) : isProcessing ? (
                    <span className="flex items-center gap-1 text-[10px] font-mono text-amber-600 bg-amber-50 px-2 py-0.5 rounded border border-amber-100 animate-pulse">
                      <Loader2 className="w-2.5 h-2.5 animate-spin" />
                      Running...
                    </span>
                  ) : (
                    <span className="text-[10px] font-mono text-slate-400 bg-slate-50 px-2 py-0.5 rounded border border-slate-100">
                      Pending
                    </span>
                  )}
                </div>

                {/* Card Data Grid */}
                <div
                  className={`grid grid-cols-[80px_1fr] gap-x-2 gap-y-1 text-[10px] pt-1.5 border-t mt-1.5 transition-colors duration-300 ${
                    agent.highlight ? "border-rose-200" : "border-slate-200"
                  }`}
                >
                  {agent.data.map((row, idx) => (
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
