import React from 'react';
import usePromptGateStore from '../../store/usePromptGateStore';
import { TrendingDown, Coins, Zap } from 'lucide-react';

export default function CostSimulator() {
  const { tokenMetrics } = usePromptGateStore();

  const isSimulated = tokenMetrics.savedTokens > 0;

  return (
    <div className="p-6 bg-dark-card rounded-2xl border border-dark-border shadow-lg">
      <div className="flex items-center gap-2 mb-4">
        <Zap className="text-yellow-500" size={20} />
        <h3 className="font-semibold text-text-primary">Token Cost Simulator</h3>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-[#1A1A1A] rounded-xl p-4 border border-dark-border">
          <p className="text-xs text-text-secondary mb-1">Direct API Cost</p>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-text-primary">${tokenMetrics.directCostUsd.toFixed(4)}</span>
          </div>
        </div>
        
        <div className="bg-brand-primary/10 rounded-xl p-4 border border-brand-primary/30 relative overflow-hidden">
          {isSimulated && (
            <div className="absolute top-0 right-0 p-2">
              <span className="flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-brand-primary"></span>
              </span>
            </div>
          )}
          <p className="text-xs text-brand-primary font-medium mb-1">PromptGate Opimized</p>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">${tokenMetrics.optimizedCostUsd.toFixed(4)}</span>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-dark-border flex items-center justify-between">
        <div className="flex flex-col">
           <div className="flex items-center gap-1 text-green-400 font-medium">
             <TrendingDown size={16} />
             <span className="text-sm">Tokens Saved</span>
           </div>
           <span className="text-2xl font-bold text-white mt-1">{tokenMetrics.savedTokens.toLocaleString()} <span className="text-xs text-text-secondary font-normal">tokens</span></span>
        </div>
        
        <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center text-green-400">
          <Coins size={24} />
        </div>
      </div>
    </div>
  );
}
