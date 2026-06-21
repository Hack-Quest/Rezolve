import React, { useState, useEffect } from "react";
/* import Header from "@/components/Header"; */
import RawLogFeed from "./RawLogFeed";
import AgentPipeline from "./AgentPipeline";
import ExecutiveBrief from "./ExecutiveBrief";
import { AnimatePresence, motion } from "framer-motion";

export default function Page() {
  const [pipelineStep, setPipelineStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);

  // Auto-advance through states (0 to 4) over 12 seconds
  // 12 seconds / 4 steps = 3 seconds per step
  useEffect(() => {
    let timer; // Removed TypeScript ": NodeJS.Timeout" type annotation
    if (isPlaying && pipelineStep < 4) {
      timer = setTimeout(() => {
        setPipelineStep((prev) => prev + 1);
      }, 3000);
    }
    return () => clearTimeout(timer);
  }, [pipelineStep, isPlaying]);

  const handleTriggerDemo = () => {
    // Restart the simulation
    setPipelineStep(0);
    setIsPlaying(true);
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-100 font-sans">
      {/* Central State Header */}
      {/*       <Header pipelineStep={pipelineStep} onTriggerDemo={handleTriggerDemo} /> */}

      {/* Main Grid Area */}
      <main className="flex-1 min-h-0 p-4">
        <div className="grid grid-cols-12 gap-4 h-full">
          {/* Column 1: Raw Log Feed (Always visible) */}
          <RawLogFeed />

          {/* Column 2: Agent Pipeline (Visible when pipelineStep >= 1) */}
          <AnimatePresence mode="wait">
            {pipelineStep >= 1 && (
              <motion.div
                key="agent-pipeline-wrapper"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
                className="col-span-5 h-full flex flex-col min-h-0"
              >
                <AgentPipeline pipelineStep={pipelineStep} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Column 3: Executive Decision Brief (Visible when pipelineStep === 4) */}
          <AnimatePresence mode="wait">
            {pipelineStep === 4 && (
              <motion.div
                key="executive-brief-wrapper"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ type: "spring", stiffness: 100, damping: 15 }}
                className="col-span-4 h-full flex flex-col min-h-0"
              >
                <ExecutiveBrief />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
