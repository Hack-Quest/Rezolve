import React from "react";
import { Terminal } from "lucide-react";
import { motion } from "framer-motion";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.2 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -10 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { type: "spring", stiffness: 100, damping: 15 },
  },
};

/**
 * RawLogFeed
 *
 * Props:
 *   rawAlert : string | null — the raw_alert text from pipeline_start SSE event.
 *              When null (before stream starts), shows the hardcoded demo log.
 */
export default function RawLogFeed({ rawAlert }) {
  return (
    <div className="col-span-3 h-full flex flex-col min-h-0 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Title block */}
      <div className="shrink-0 p-3 border-b border-slate-100 font-bold text-slate-800 uppercase tracking-wider text-xs flex justify-between items-center">
        <div className="flex items-center gap-2">
          01 // WHAT CAME IN
          <Terminal className="w-3.5 h-3.5 text-slate-400" />
        </div>
        <span className="text-[10px] font-mono text-slate-400">
          INC-2024-1138
        </span>
      </div>

      {/* Terminal Content */}
      <motion.div
        key={rawAlert ?? "placeholder"}
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="flex-1 overflow-y-auto min-h-0 p-3 bg-[#0f172a] text-[11px] font-mono text-slate-300 leading-relaxed terminal-scroll select-none"
      >
        {rawAlert ? (
          /* Live alert text from SSE pipeline_start */
          <>
            <motion.div
              variants={itemVariants}
              className="text-slate-500 mb-3 border-b border-slate-800 pb-2"
            >
              SOURCE: Rezolve Decision Engine
              <br />
              TIME: {new Date().toISOString().replace("T", " ").slice(0, 19)} UTC
              <br />
              <span className="text-rose-500 font-bold">PIPELINE · Active</span>
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="log-entry-new text-rose-400 font-bold p-1 -mx-1 rounded whitespace-pre-wrap break-words"
            >
              &gt; {rawAlert}
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="animate-pulse mt-4 text-slate-500 font-bold"
            >
              _
            </motion.div>
          </>
        ) : (
          /* Placeholder shown while stream hasn't started yet */
          <>
            <motion.div
              variants={itemVariants}
              className="text-slate-500 mb-3 border-b border-slate-800 pb-2"
            >
              SOURCE: Splunk Enterprise Security
              <br />
              TIME: 2024-11-08 14:32:08 UTC
              <br />
              <span className="text-rose-500 font-bold">P1 · Critical</span>
            </motion.div>

            <motion.div variants={itemVariants} className="opacity-70">
              [14:31:55] TCP_CONN REQ src=198.51.100.42 port=8080
            </motion.div>

            <motion.div variants={itemVariants} className="opacity-70 mt-1">
              [14:32:01] SSL_HANDSHAKE success protocol=TLSv1.3
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="text-amber-400 mt-2 font-semibold"
            >
              &gt; WARN: Unusual payload size detected
            </motion.div>

            <motion.div variants={itemVariants} className="opacity-70 mt-1">
              [14:32:05] HTTP_GET /struts2-showcase/index.action
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="log-entry-new text-rose-400 mt-2 font-bold p-1 -mx-1 rounded"
            >
              &gt; CRITICAL ALERT: Unauthorized database access attempt via Apache
              Struts on port 8080 from IP 198.51.100.42.
            </motion.div>

            <motion.div variants={itemVariants} className="opacity-70 mt-2">
              [14:32:09] IDS_RULE_MATCH sig_id=2024312
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="animate-pulse mt-4 text-slate-500 font-bold"
            >
              _
            </motion.div>
          </>
        )}
      </motion.div>
    </div>
  );
}
