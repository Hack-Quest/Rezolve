import React from "react";

export default function Pipeline() {
  return (
    // REMOVED style={{ opacity: 0 }} so that the CSS .reveal class can drive the opacity animation smoothly
    <section className="max-w-7xl mx-auto px-gutter mt-16 md:mt-24 mb-16 reveal delay-200">
      {/* Header Summary */}
      <div className="text-center mb-16 space-y-md">
        <h2 className="font-headline font-extrabold text-4xl text-on-surface">
          The 4-Agent Inference Pipeline
        </h2>
        <p className="text-slate-600 text-lg max-w-2xl mx-auto font-body">
          Specialized AI agents working in parallel to eliminate noise and
          synthesize strategy.
        </p>
      </div>

      {/* 4-Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter">
        {/* Agent 1: Scout */}
        <div className="bg-white relative z-10 overflow-hidden p-8 rounded-lg border border-outline-variant shadow-sm hover:shadow-md transition-all group min-h-[320px] flex flex-col">
          <div className="relative z-10 flex flex-col h-full">
            <div className="w-12 h-12 bg-rose-50 rounded-lg flex items-center justify-center mb-6">
              <span className="material-symbols-outlined text-primary">
                search
              </span>
            </div>
            <h3 className="font-headline font-bold text-xl mb-3 text-on-surface">
              Scout
            </h3>
            <p className="text-sm text-slate-600 mb-6 font-body leading-relaxed">
              Initial intake agent. Scans raw telemetry and logs for anomalous
              patterns and known threat signatures.
            </p>
            <div className="mt-auto pt-4 border-t border-rose-100 font-mono text-[11px] text-primary flex justify-between">
              <span>Stage:</span>
              <span className="font-bold">Entity Extraction</span>
            </div>
          </div>
        </div>

        {/* Agent 2: Investigator */}
        <div className="bg-white relative z-10 overflow-hidden p-8 rounded-lg border border-outline-variant shadow-sm hover:shadow-md transition-all group min-h-[320px] flex flex-col">
          <div className="relative z-10 flex flex-col h-full">
            <div className="w-12 h-12 bg-slate-50 rounded-lg flex items-center justify-center mb-6 group-hover:bg-rose-50 transition-colors">
              <span className="material-symbols-outlined text-slate-600 group-hover:text-primary">
                troubleshoot
              </span>
            </div>
            <h3 className="font-headline font-bold text-xl mb-3 text-on-surface">
              Investigator
            </h3>
            <p className="text-sm text-slate-600 mb-6 font-body leading-relaxed">
              Contextual enrichment layer. Cross-references alerts with global
              threat intelligence and internal asset maps.
            </p>
            <div className="mt-auto pt-4 border-t border-rose-100 font-mono text-[11px] text-primary flex justify-between">
              <span>Stage:</span>
              <span className="font-bold">CVE Diagnosis</span>
            </div>
          </div>
        </div>

        {/* Agent 3: Impact */}
        <div className="bg-white relative z-10 overflow-hidden p-8 rounded-lg border border-outline-variant shadow-sm hover:shadow-md transition-all group min-h-[320px] flex flex-col">
          <div className="relative z-10 flex flex-col h-full">
            <div className="w-12 h-12 bg-rose-50 rounded-lg flex items-center justify-center mb-6">
              <span className="material-symbols-outlined text-primary">
                analytics
              </span>
            </div>
            <h3 className="font-headline font-bold text-xl mb-3 text-on-surface">
              Impact
            </h3>
            <p className="text-sm text-slate-600 mb-6 font-body leading-relaxed">
              Quantifies business risk. Translates technical vulnerabilities
              into potential financial and operational loss.
            </p>
            <div className="mt-auto pt-4 border-t border-rose-100 font-mono text-[11px] text-primary flex justify-between">
              <span>Stage:</span>
              <span className="font-bold">Business Impact</span>
            </div>
          </div>
        </div>

        {/* Agent 4: Commander */}
        <div className="bg-white relative z-10 overflow-hidden p-8 rounded-lg border border-outline-variant shadow-sm hover:shadow-md transition-all group min-h-[320px] flex flex-col">
          <div className="relative z-10 flex flex-col h-full">
            <div className="w-12 h-12 bg-slate-50 rounded-lg flex items-center justify-center mb-6 group-hover:bg-rose-50 transition-colors">
              <span className="material-symbols-outlined text-slate-600 group-hover:text-primary">
                gavel
              </span>
            </div>
            <h3 className="font-headline font-bold text-xl mb-3 text-on-surface">
              Commander
            </h3>
            <p className="text-sm text-slate-600 mb-6 font-body leading-relaxed">
              The final synthesis layer. Generates actionable directives and
              executive-ready summary briefs.
            </p>
            <div className="mt-auto pt-4 border-t border-rose-100 font-mono text-[11px] text-primary flex justify-between">
              <span>Stage:</span>
              <span className="font-bold">Action Synthesis</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
