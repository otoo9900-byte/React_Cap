import React, { useState, useRef, useEffect } from 'react';
import usePromptGateStore from '../../store/usePromptGateStore';
import { TrendingDown, Coins, Zap, X } from 'lucide-react';

export default function CostSimulator() {
  const { tokenMetrics } = usePromptGateStore();
  const [isOpen, setIsOpen] = useState(false);
  const popupRef = useRef(null);

  const isSimulated = tokenMetrics.savedTokens > 0;

  // Close when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={popupRef}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 bg-dark-card border border-dark-border rounded-lg hover:border-brand-primary/50 hover:bg-dark-hover transition-colors text-sm text-text-primary shadow-sm"
      >
        <Zap className="text-yellow-500" size={16} />
        <span>Savings: <span className="font-bold text-green-400">{tokenMetrics.savedTokens.toLocaleString()}</span></span>
      </button>

      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-80 p-5 bg-dark-card rounded-2xl border border-dark-border shadow-2xl z-50">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Zap className="text-yellow-500" size={18} />
              <h3 className="font-semibold text-text-primary text-sm">Token Cost Simulator</h3>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-text-secondary hover:text-white transition-colors">
              <X size={16} />
            </button>
          </div>
          
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-[#1A1A1A] rounded-xl p-3 border border-dark-border">
              <p className="text-[10px] text-text-secondary mb-1 uppercase tracking-wider font-medium">Direct API</p>
              <div className="flex items-baseline gap-1">
                <span className="text-lg font-bold text-text-primary">${tokenMetrics.directCostUsd.toFixed(4)}</span>
              </div>
            </div>
            
            <div className="bg-brand-primary/10 rounded-xl p-3 border border-brand-primary/30 relative overflow-hidden">
              {isSimulated && (
                <div className="absolute top-0 right-0 p-1.5">
                  <span className="flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-primary opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-primary"></span>
                  </span>
                </div>
              )}
              <p className="text-[10px] text-brand-primary font-bold mb-1 uppercase tracking-wider">PromptGate</p>
              <div className="flex items-baseline gap-1">
                <span className="text-lg font-bold text-white">${tokenMetrics.optimizedCostUsd.toFixed(4)}</span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-dark-border flex items-center justify-between">
            <div className="flex flex-col">
               <div className="flex items-center gap-1 text-green-400 font-medium">
                 <TrendingDown size={14} />
                 <span className="text-xs">Tokens Saved</span>
               </div>
               <span className="text-2xl font-bold text-white mt-1">{tokenMetrics.savedTokens.toLocaleString()}</span>
            </div>
            
            <div className="w-10 h-10 rounded-full bg-green-500/20 flex items-center justify-center text-green-400">
              <Coins size={20} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
