import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="px-gutter reveal" style={{ opacity: 1 }}>
      <div className="w-full max-w-7xl mx-auto min-h-[75vh] rounded-[2.5rem] overflow-hidden relative shadow-xl border border-slate-200 bg-white flex flex-col lg:flex-row items-center">
        {/* Background Image Layer */}
        <div
          className="absolute inset-0 z-0 bg-cover bg-center"
          style={{
            backgroundImage:
              "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCbH9zYq_rgRrU5JDhcOZDhoJSewXpVkb5LNrufGZA4MDeD5z3MHKUUWhitOPLyXrujUsbeXFI3Bu_dQxHlmHNENzBuX0et6-GxIIwmsp21SY1TtHPlLtnCQK232au0ZkT-2745X2g6DDe6e0QNxBr6HnEmsbVfVKMIIP600R-H0VNl4YwMDcbu0RuP9BRCPWmJvt-apwdEDlcr3UAo8yi85-b1-gG8l1s_S-O5ddpNnnieOVTdAHfxYFJgz24PFKYlpvQdJmrq7D0')",
          }}
        />

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-white via-white/90 to-transparent z-0" />

        {/* Content Grid */}
        <div className="relative z-10 w-full h-full grid grid-cols-1 lg:grid-cols-2 gap-xl p-7 md:p-14">
          {/* Left Text Column */}
          <div className="flex flex-col justify-center space-y-lg relative z-10">
            <div className="inline-flex items-center gap-2 bg-rose-50 text-rose-600 px-4 py-1.5 rounded-full text-sm font-bold tracking-tight border border-rose-100 self-start">
              <span>✨ ELEVATE HACKATHON INNOVATION</span>
            </div>

            <h1 className="font-headline font-extrabold text-4xl md:text-5xl leading-[1.1] tracking-tight">
              From Noise to Decision.
              <br />
              <span className="text-primary italic">In Seconds.</span>
            </h1>

            <p className="text-slate-600 text-lg max-w-xl font-body">
              A multi-agent AI pipeline that turns chaotic security alerts into
              executive action briefs. Eliminate cognitive load with specialized
              inference specialization.
            </p>

            <div className="flex flex-wrap gap-md pt-8">
              <Link
                to="/demo"
                className="bg-primary text-white px-10 py-5 rounded-2xl font-headline font-bold text-lg hover:bg-primary/90 transition-all shadow-lg shadow-rose-200 cursor-pointer inline-flex items-center justify-center"
              >
                Live Demo
              </Link>
            </div>
          </div>

          {/* Right Dashboard Status Column */}
          <div className="hidden lg:flex items-center justify-center relative">
            {/* Glassmorphic Dashboard Panel */}
            {/* Right Floating Status Panel */}
            <div className="hidden lg:flex items-center justify-center relative">
              {/* Outer Glow */}
              <div className="absolute w-[550px] h-[350px] bg-rose-300/20 blur-3xl rounded-full" />

              {/* Floating Glass Card */}
              <div
                className="relative animate-float w-[580px] rounded-[28px]
      bg-white/25
      backdrop-blur-2xl
      border border-white/40
      shadow-[0_20px_80px_rgba(0,0,0,0.12)]
      p-10"
              >
                {/* Header */}
                <div className="flex justify-between items-center mb-10">
                  <div className="flex items-center gap-4">
                    <div className="w-4 h-4 bg-emerald-500 rounded-full animate-pulse" />

                    <span className="font-mono uppercase tracking-[0.25em] text-slate-500 text-sm font-bold">
                      System Status: Live
                    </span>
                  </div>

                  <div className="flex gap-1">
                    <div className="w-1.5 h-1.5 bg-slate-400 rounded-full" />
                    <div className="w-1.5 h-1.5 bg-slate-400 rounded-full" />
                    <div className="w-1.5 h-1.5 bg-slate-400 rounded-full" />
                  </div>
                </div>

                {/* SCOUT */}
                <div className="mb-8">
                  <div className="flex justify-between mb-3">
                    <span className="font-mono text-slate-600 font-bold">
                      SCOUT
                    </span>

                    <span className="font-mono text-slate-500">
                      Ingesting data...
                    </span>
                  </div>

                  <div className="h-2 bg-slate-200/50 rounded-full overflow-hidden">
                    <div className="h-full w-[72%] bg-emerald-500 rounded-full" />
                  </div>
                </div>

                {/* INVESTIGATOR */}
                <div className="mb-8">
                  <div className="flex justify-between mb-3">
                    <span className="font-mono text-slate-600 font-bold">
                      INVESTIGATOR
                    </span>

                    <span className="font-mono text-slate-500">
                      Analyzing CVEs...
                    </span>
                  </div>

                  <div className="h-2 bg-slate-200/50 rounded-full overflow-hidden">
                    <div className="h-full w-[45%] bg-rose-600 rounded-full" />
                  </div>
                </div>

                {/* COMMANDER */}
                <div className="mb-10">
                  <div className="flex justify-between mb-3">
                    <span className="font-mono text-slate-600 font-bold">
                      COMMANDER
                    </span>

                    <span className="font-mono text-slate-500">
                      Ready for Briefing.
                    </span>
                  </div>

                  <div className="h-2 bg-slate-200/50 rounded-full overflow-hidden">
                    <div className="h-full w-[10%] bg-slate-300 rounded-full" />
                  </div>
                </div>

                {/* Bottom Blocks */}
                <div className="border-t border-white/30 pt-8 flex justify-between">
                  <div className="h-12 w-32 rounded-xl bg-rose-100/70" />

                  <div className="h-12 w-32 rounded-xl bg-white/70" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
