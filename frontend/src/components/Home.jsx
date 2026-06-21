import React from 'react';

export default function Home() {
  return (
    <section className="px-gutter reveal" style={{ opacity: 1 }}>
      <div className="w-full max-w-7xl mx-auto min-h-[75vh] rounded-[2.5rem] overflow-hidden relative shadow-xl border border-slate-200 bg-white flex flex-col lg:flex-row items-center">
        
        {/* Background Image Layer */}
        <div
          className="absolute inset-0 z-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCbH9zYq_rgRrU5JDhcOZDhoJSewXpVkb5LNrufGZA4MDeD5z3MHKUUWhitOPLyXrujUsbeXFI3Bu_dQxHlmHNENzBuX0et6-GxIIwmsp21SY1TtHPlLtnCQK232au0ZkT-2745X2g6DDe6e0QNxBr6HnEmsbVfVKMIIP600R-H0VNl4YwMDcbu0RuP9BRCPWmJvt-apwdEDlcr3UAo8yi85-b1-gG8l1s_S-O5ddpNnnieOVTdAHfxYFJgz24PFKYlpvQdJmrq7D0')",
          }}
        />
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-white via-white/90 to-transparent z-0" />
        
        {/* Content Grid */}
        <div className="relative z-10 w-full h-full grid grid-cols-1 lg:grid-cols-2 gap-xl p-8 md:p-16">
          
          {/* Left Text Column */}
          <div className="flex flex-col justify-center space-y-lg relative z-10">
            <div className="inline-flex items-center gap-2 bg-rose-50 text-rose-600 px-4 py-1.5 rounded-full text-sm font-bold tracking-tight border border-rose-100 self-start">
              <span>✨ ELEVATE HACKATHON INNOVATION</span>
            </div>
            
            <h1 className="font-headline font-extrabold text-5xl md:text-6xl text-on-surface leading-[1.1] tracking-tight">
              From Noise to Decision.<br />
              <span className="text-primary italic">In Seconds.</span>
            </h1>
            
            <p className="text-slate-600 text-lg max-w-xl font-body">
              A multi-agent AI pipeline that turns chaotic security alerts
              into executive action briefs. Eliminate cognitive load with
              specialized inference specialization.
            </p>
            
            <div className="flex flex-wrap gap-md pt-4">
              <button className="bg-primary text-white px-xl py-4 rounded-xl font-headline font-bold text-lg hover:bg-primary/90 transition-all shadow-lg shadow-rose-200 cursor-pointer">
                Live Demo
              </button>
              <button className="bg-white text-slate-700 border-2 border-slate-200 px-xl py-4 rounded-xl font-headline font-bold text-lg hover:bg-slate-50 transition-all cursor-pointer">
                Documentation
              </button>
            </div>
          </div>

          {/* Right Dashboard Status Column */}
          <div className="hidden lg:flex items-center justify-center relative">
            
            {/* Glassmorphic Dashboard Panel */}
            <div className="animate-float bg-white/40 backdrop-blur-xl border border-white/60 shadow-2xl rounded-2xl p-8 w-full max-w-md relative overflow-hidden">
              
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="font-mono text-xs font-bold text-slate-500 uppercase tracking-widest">
                    System Status: Live
                  </span>
                </div>
                <span className="material-symbols-outlined text-slate-400">
                  more_horiz
                </span>
              </div>

              <div className="space-y-6">
                {/* Scout Agent Progress */}
                <div className="space-y-2">
                  <div className="flex justify-between text-[11px] font-mono font-bold text-slate-600">
                    <span>SCOUT</span>
                    <span>Ingesting data...</span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-200/50 rounded-full overflow-hidden">
                    <div className="h-full w-[70%] bg-emerald-500 rounded-full" />
                  </div>
                </div>

                {/* Investigator Agent Progress */}
                <div className="space-y-2">
                  <div className="flex justify-between text-[11px] font-mono font-bold text-slate-600">
                    <span>INVESTIGATOR</span>
                    <span>Analyzing CVEs...</span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-200/50 rounded-full overflow-hidden">
                    <div className="h-full w-[45%] bg-rose-600 rounded-full" />
                  </div>
                </div>

                {/* Commander Agent Progress */}
                <div className="space-y-2">
                  <div className="flex justify-between text-[11px] font-mono font-bold text-slate-600">
                    <span>COMMANDER</span>
                    <span>Ready for Briefing.</span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-200/50 rounded-full overflow-hidden">
                    <div className="h-full w-0 bg-slate-400 rounded-full" />
                  </div>
                </div>

                {/* Bottom Placeholder Accents */}
                <div className="pt-4 border-t border-slate-200/50 flex justify-between">
                  <div className="h-8 w-24 bg-rose-100/60 rounded-lg" />
                  <div className="h-8 w-24 bg-slate-100/60 rounded-lg" />
                </div>
              </div>

              {/* Glowing Decorative Particle */}
              <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-primary/10 rounded-full blur-2xl" />
            </div>

          </div>

        </div>
      </div>
    </section>

    
  );
}