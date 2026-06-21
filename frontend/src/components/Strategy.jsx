import React from "react";

export default function Strategy() {
  return (
    <section
      className="mt-12 md:mt-24 py-12 md:py-24 bg-[#fff8f7] border-y border-rose-100/40"
      id="strategy"
    >
      <div className="max-w-7xl mx-auto px-gutter">
        {/* Section Heading */}
        <div className="mb-12">
          <h2 className="font-headline font-extrabold text-3xl text-on-surface tracking-tight">
            OPERATIONAL STRATEGY
          </h2>
          <div className="h-1 w-20 bg-primary mt-4" />
        </div>

        {/* Content Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-lg">
          {/* Core Problem Card */}
          <div className="bg-white p-6 md:p-8 rounded-2xl border border-rose-100 shadow-sm flex flex-col gap-4">
            <h3 className="font-headline text-xl font-semibold text-primary">
              Core Problem
            </h3>
            <p className="text-slate-600 font-body leading-relaxed">
              Traditional security setups drown in chaotic data streams where
              critical signals are lost in the noise. Relying on a single
              generalist LLM often leads to hallucinations and structural
              failure under high-volume stress.
            </p>
          </div>

          {/* Multi-Agent Solution Card */}
          <div className="bg-white p-6 md:p-8 rounded-2xl border border-rose-100 shadow-sm flex flex-col gap-4">
            <h3 className="font-headline text-xl font-semibold text-primary">
              Multi-Agent Solution
            </h3>
            <p className="text-slate-600 font-body leading-relaxed">
              REZOLVE employs specialized agents mirroring a high-stakes War
              Room. Each node in the pipeline is optimized for a specific
              cognitive task, ensuring precision and accountability at every
              stage of the decision-making cycle.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
