import React from 'react';
import ChatInterface from '../components/Chat/ChatInterface';
import CostSimulator from '../components/Dashboard/CostSimulator';
import PromptAssembler from '../components/ResultView/PromptAssembler';
import usePromptGateStore from '../store/usePromptGateStore';
import { RefreshCcw } from 'lucide-react';

export default function Main() {
  const { resetSession } = usePromptGateStore();

  return (
    <div className="flex w-full h-[calc(100vh-64px)] bg-dark-bg text-text-primary overflow-hidden">
      {/* Left Pane: Agentic Chat */}
      <div className="w-1/3 min-w-[350px] max-w-[500px]">
        <ChatInterface />
      </div>

      {/* Right Pane: Dashboard & Result */}
      <div className="flex-1 flex flex-col p-6 gap-6 overflow-y-auto bg-dark-bg">
        {/* Header toolbar */}
        <div className="flex items-center justify-between mb-2">
          <div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-brand-primary to-brand-secondary">
              Workspace
            </h1>
            <p className="text-sm text-text-secondary mt-1">PromptGate 최적화 세션</p>
          </div>
          <div className="flex items-center gap-3">
            <CostSimulator />
            <button 
               onClick={resetSession}
               className="flex items-center gap-2 px-3 py-2 text-sm text-text-secondary hover:text-text-primary border border-dark-border hover:bg-dark-card rounded-lg transition-colors shadow-sm"
            >
               <RefreshCcw size={16} />
               New Session
            </button>
          </div>
        </div>

        {/* Result Area */}
        <div className="flex-1 mt-2 mb-8">
           <PromptAssembler />
        </div>
      </div>
    </div>
  );
}
