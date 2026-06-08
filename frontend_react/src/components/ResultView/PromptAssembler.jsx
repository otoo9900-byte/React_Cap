import React, { useState } from 'react';
import usePromptGateStore from '../../store/usePromptGateStore';
import { Play, CheckCircle2, Sparkles, AlertCircle, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
export default function PromptAssembler() {
  const { assembledPrompt, intents, finalResult, isExecuting, runAssembledPrompt } = usePromptGateStore();
  const [activeTab, setActiveTab] = useState('prompt'); // 'prompt' or 'result'

  const handleExecute = async () => {
    setActiveTab('result'); // Switch tab immediately to show loading
    await runAssembledPrompt();
  };

  if (!assembledPrompt) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center bg-dark-card rounded-2xl border border-dark-border shadow-lg">
        <Sparkles size={48} className="text-brand-secondary/30 mb-4" />
        <h3 className="text-lg font-medium text-text-secondary mb-2">프롬프트 조립 대기 중</h3>
        <p className="text-sm text-text-secondary w-2/3">좌측 채팅에서 AI와 대화를 완료하면 이곳에 전문가 수준의 프롬프트가 완성됩니다.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-dark-card rounded-2xl border border-brand-secondary/30 shadow-[0_0_30px_rgba(139,92,246,0.1)] relative overflow-hidden">
      {/* Header with Tabs */}
      <div className="p-4 border-b border-dark-border flex items-center justify-between bg-brand-secondary/5">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-brand-secondary/20 rounded-md">
              <Sparkles size={18} className="text-brand-secondary" />
            </div>
            <h3 className="font-semibold text-text-primary">Workspace</h3>
          </div>
          
          {/* Tabs */}
          <div className="flex bg-dark-bg p-1 rounded-lg">
            <button
              onClick={() => setActiveTab('prompt')}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeTab === 'prompt' ? 'bg-dark-card text-white shadow-sm' : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Prompt
            </button>
            <button
              onClick={() => setActiveTab('result')}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeTab === 'result' ? 'bg-brand-primary text-white shadow-sm' : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              Final Result
            </button>
          </div>
        </div>

        {activeTab === 'prompt' && (
          <button 
            onClick={handleExecute}
            disabled={isExecuting}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-brand-primary hover:bg-blue-600 disabled:bg-gray-600 text-white rounded-lg transition-colors"
          >
            {isExecuting ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
            {isExecuting ? 'Executing...' : 'Execute AI'}
          </button>
        )}
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto flex flex-col">
        {activeTab === 'prompt' ? (
          <>
            {/* Intents Meta */}
            {intents && (
               <div className="px-5 pt-4 pb-2 flex flex-wrap gap-2">
                  {Object.entries(intents).map(([key, value]) => (
                     <div key={key} className="px-2 py-1 text-xs bg-dark-border text-text-secondary rounded-md capitalize border border-[#333]">
                       {key}: <span className="text-text-primary ml-1">{value}</span>
                     </div>
                  ))}
               </div>
            )}
            
            {/* Code Viewer */}
            <div className="flex-1 p-5">
              <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-[#A5B4FC]">
                {assembledPrompt}
              </pre>
            </div>
          </>
        ) : (
          /* Final Result Viewer */
          <div className="flex-1 p-6 relative">
            {isExecuting ? (
              <div className="h-full flex flex-col items-center justify-center text-center">
                <Loader2 size={40} className="animate-spin text-brand-primary mb-4" />
                <h3 className="text-lg font-medium text-text-primary mb-2">AI가 결과물을 생성 중입니다...</h3>
                <p className="text-sm text-text-secondary">이 작업은 약 5~15초 정도 소요될 수 있습니다.</p>
              </div>
            ) : finalResult ? (
              <div className="prose prose-invert max-w-none text-sm text-gray-200">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {finalResult}
                </ReactMarkdown>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center">
                <Sparkles size={40} className="text-text-secondary/50 mb-4" />
                <p className="text-sm text-text-secondary">아직 실행된 결과가 없습니다.<br/>'Prompt' 탭에서 [Execute AI] 버튼을 눌러보세요.</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer Alert */}
      {activeTab === 'prompt' && (
        <div className="p-3 bg-brand-primary/10 border-t border-brand-primary/20 flex items-start gap-2 text-xs text-blue-200">
           <AlertCircle size={14} className="mt-0.5 shrink-0 text-brand-primary" />
           <p>PII 자동 마스킹 및 CoT 최적화가 적용된 최종 프롬프트입니다. [Execute AI]를 눌러 모델로 전송하세요.</p>
        </div>
      )}
    </div>
  );
}
