"use client";

import React from "react";
import { ListChecks, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

/**
 * ExecutiveBrief
 *
 * Props:
 *   results : PipelineResults envelope from pipeline_complete SSE event
 *     {
 *       scout:        { target, attacker_ip, action }
 *       investigator: { diagnosis, confidence_score }
 *       impact:       { severity, affected_asset, potential_damage }
 *       commander:    { summary_headline, recommended_actions: string[] }
 *     }
 */
export default function ExecutiveBrief({ results }) {
  if (!results) return null;

  const { investigator, impact, commander } = results;
  const actions = commander?.recommended_actions ?? [];
  const confidenceScore = investigator?.confidence_score ?? 0;

  // Color the severity badge
  const severityColor =
    impact?.severity === "CRITICAL"
      ? "text-rose-600"
      : impact?.severity === "HIGH"
        ? "text-orange-600"
        : impact?.severity === "MEDIUM"
          ? "text-amber-600"
          : "text-emerald-600";

  // Priority tags rotate: P0 for first two, P1 for rest
  function priorityTag(idx) {
    return idx < 2 ? (
      <span className="text-[9px] font-mono text-rose-600 bg-rose-50 border border-rose-100 px-1 py-0.5 rounded font-bold">
        priority p0
      </span>
    ) : (
      <span className="text-[9px] font-mono text-amber-600 bg-amber-50 border border-amber-100 px-1 py-0.5 rounded font-bold">
        priority p1
      </span>
    );
  }

  return (
    <div className="col-span-4 h-full flex flex-col min-h-0 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden select-none">
      {/* Title Header */}
      <div className="shrink-0 p-3 border-b border-slate-100 font-bold text-slate-800 uppercase tracking-wider text-xs bg-slate-50 flex justify-between items-center">
        <span>03 // WHAT TO DO</span>
        <ListChecks className="w-4 h-4 text-slate-400" />
      </div>

      {/* Main Contents */}
      <div className="flex-1 overflow-y-auto min-h-0 p-4 flex flex-col gap-3">

        {/* KPI Cards Grid */}
        <div className="grid grid-cols-2 gap-2 shrink-0">
          {/* Severity */}
          <div className="bg-white border border-slate-200 rounded-lg p-2.5 flex flex-col justify-center shadow-sm">
            <span className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
              Severity
            </span>
            <span className={`text-lg font-bold ${severityColor}`}>
              {impact?.severity ?? "—"}
            </span>
            <span className="block text-[9px] font-mono text-slate-500 mt-1 leading-tight">
              {investigator?.diagnosis?.slice(0, 36) ?? ""}
            </span>
          </div>

          {/* Confidence */}
          <div className="bg-white border border-slate-200 rounded-lg p-2.5 flex flex-col justify-center shadow-sm">
            <span className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
              Confidence
            </span>
            <span className="text-lg font-bold text-slate-900">
              {confidenceScore}%
            </span>
            <div className="w-full bg-slate-100 h-1 mt-1.5 rounded-full overflow-hidden shrink-0">
              <div
                className="bg-slate-800 h-full rounded-full transition-all duration-700"
                style={{ width: `${confidenceScore}%` }}
              />
            </div>
          </div>

          {/* Affected Asset */}
          <div className="bg-white border border-slate-200 rounded-lg p-2.5 relative overflow-hidden shadow-sm">
            <div className="absolute right-1 top-1">
              <span className="text-[7px] font-mono font-bold text-rose-600 bg-rose-50 border border-rose-100 px-1 py-0.5 rounded">
                AI-synthesized
              </span>
            </div>
            <span className="block text-[9px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
              Affected Asset
            </span>
            <span className="text-[13px] font-bold text-slate-900 leading-tight block truncate">
              {impact?.affected_asset ?? "—"}
            </span>
          </div>

          {/* Potential Damage */}
          <div className="bg-white border border-slate-200 rounded-lg p-2.5 relative overflow-hidden shadow-sm">
            <div className="absolute right-1 top-1">
              <span className="text-[7px] font-mono font-bold text-rose-600 bg-rose-50 border border-rose-100 px-1 py-0.5 rounded">
                AI-synthesized
              </span>
            </div>
            <span className="block text-[9px] font-semibold text-slate-500 uppercase tracking-wider mb-1 truncate">
              Potential Damage
            </span>
            <span className="text-[13px] font-bold text-slate-900 leading-tight block truncate">
              {impact?.potential_damage ?? "—"}
            </span>
          </div>
        </div>

        {/* Commander Headline — "Wow" callout box */}
        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 100, damping: 12, delay: 0.1 }}
          className="bg-rose-50/50 border border-rose-200 rounded-lg p-3 relative overflow-hidden shrink-0 shadow-sm"
        >
          <div className="absolute left-0 top-0 bottom-0 w-1 bg-rose-500" />
          <div className="flex items-start gap-2 pl-1">
            <div className="bg-rose-600 rounded pt-0.5 pb-0.5 px-1 shrink-0 mt-0.5">
              <Sparkles className="w-3 h-3 text-white" />
            </div>
            <div>
              <h4 className="text-xs text-rose-700 font-bold mb-1 tracking-wide uppercase">
                Commander's Verdict
              </h4>
              <p className="text-[10px] text-slate-600 leading-relaxed">
                {commander?.summary_headline ?? "—"}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Recommended Actions */}
        <div className="flex-grow flex flex-col shrink-0">
          <div className="flex justify-between items-end mb-2 border-b border-slate-200 pb-1">
            <h4 className="text-[11px] text-slate-900 font-bold uppercase tracking-wide">
              Recommended Actions
            </h4>
            <span className="text-[9px] font-mono text-slate-400">by Commander</span>
          </div>

          <div className="flex flex-col gap-1.5">
            {actions.length === 0 ? (
              <p className="text-[10px] text-slate-400 font-mono">No actions yet.</p>
            ) : (
              actions.map((action, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 * idx }}
                  className="flex items-start gap-2 p-2 bg-white rounded-lg border border-slate-100 shadow-sm"
                >
                  <span className="text-[10px] font-mono font-bold text-slate-400 pt-0.5 border-r border-rose-500 pr-2 shrink-0">
                    {String(idx + 1).padStart(2, "0")}
                  </span>
                  <div className="flex-grow min-w-0">
                    <span className="block text-[11px] font-semibold text-slate-900 leading-snug">
                      {action}
                    </span>
                    <div className="flex items-center gap-1 mt-1 flex-wrap">
                      {priorityTag(idx)}
                    </div>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
