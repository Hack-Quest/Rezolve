"use client";

import React from "react";
import { ListChecks, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

export default function ExecutiveBrief() {
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
          <div className="bg-white border border-slate-200 rounded-lg p-2.5 flex flex-col justify-center shadow-sm">
            <span className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
              Severity
            </span>
            <span className="text-lg font-bold text-rose-600">CRITICAL</span>
            <span className="block text-[9px] font-mono text-slate-500 mt-1 leading-tight">
              CVSS 9.8 · CVE-2017-5638
            </span>
          </div>

          <div className="bg-white border border-slate-200 rounded-lg p-2.5 flex flex-col justify-center shadow-sm">
            <span className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
              Confidence
            </span>
            <span className="text-lg font-bold text-slate-900">92%</span>
            <div className="w-full bg-slate-100 h-1 mt-1.5 rounded-full overflow-hidden shrink-0">
              <div className="bg-slate-800 h-full w-[92%]"></div>
            </div>
          </div>

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
              Production Struts Gateway
            </span>
            <span className="block text-[9px] font-mono text-slate-500 mt-0.5">
              AST-PAY-0042
            </span>
          </div>

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
              5.2M records
            </span>
            <span className="block text-[9px] font-mono text-slate-500 mt-0.5 truncate">
              PCI-DSS Tier 1
            </span>
          </div>
        </div>

        {/* Wow Moment: Pink Box Slide-in with Spring Animation */}
        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 100, damping: 12, delay: 0.1 }}
          className="bg-rose-50/50 border border-rose-200 rounded-lg p-3 relative overflow-hidden shrink-0 shadow-sm"
        >
          <div className="absolute left-0 top-0 bottom-0 w-1 bg-rose-500"></div>
          <div className="flex items-start gap-2 pl-1">
            <div className="bg-rose-600 rounded pt-0.5 pb-0.5 px-1 shrink-0 mt-0.5">
              <Sparkles className="w-3 h-3 text-white" />
            </div>
            <div>
              <h4 className="text-xs text-rose-700 font-bold mb-1 tracking-wide uppercase">
                The interesting part
              </h4>
              <p className="text-[10px] text-slate-600 leading-relaxed">
                Source alert didn't specify the server or records at risk.{" "}
                <b>Impact Agent</b> correlated IP/port against asset inventory. Marked{" "}
                <b className="text-rose-600">"AI-synthesized"</b>.
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
            <div className="flex items-start gap-2 p-2 bg-white rounded-lg border border-slate-100 shadow-sm">
              <span className="text-[10px] font-mono font-bold text-slate-400 pt-0.5 border-r border-rose-500 pr-2">
                01
              </span>
              <div className="flex-grow min-w-0">
                <span className="block text-[11px] font-semibold text-slate-900 leading-snug">
                  Cut affected servers from main network.
                </span>
                <div className="flex items-center gap-1 mt-1 flex-wrap">
                  <span className="text-[9px] font-mono text-rose-600 bg-rose-50 border border-rose-100 px-1 py-0.5 rounded font-bold">
                    priority p0
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-start gap-2 p-2 bg-white rounded-lg border border-slate-100 shadow-sm">
              <span className="text-[10px] font-mono font-bold text-slate-400 pt-0.5 border-r border-rose-500 pr-2">
                02
              </span>
              <div className="flex-grow min-w-0">
                <span className="block text-[11px] font-semibold text-slate-900 leading-snug">
                  Engage IR team & open emergency channel.
                </span>
                <div className="flex items-center gap-1 mt-1 flex-wrap">
                  <span className="text-[9px] font-mono text-rose-600 bg-rose-50 border border-rose-100 px-1 py-0.5 rounded font-bold">
                    priority p0
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-start gap-2 p-2 bg-white rounded-lg border border-slate-100 shadow-sm">
              <span className="text-[10px] font-mono font-bold text-slate-400 pt-0.5 border-r border-transparent pr-2">
                03
              </span>
              <div className="flex-grow min-w-0">
                <span className="block text-[11px] font-semibold text-slate-900 leading-snug">
                  Update software or replace passwords.
                </span>
                <div className="flex items-center gap-1 mt-1 flex-wrap">
                  <span className="text-[9px] font-mono text-amber-600 bg-amber-50 border border-amber-100 px-1 py-0.5 rounded font-bold">
                    priority p1
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
