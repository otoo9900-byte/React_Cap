import React, { useState } from 'react';
import usePromptGateStore from '../../store/usePromptGateStore';
import { Copy, CheckCircle2, Sparkles, AlertCircle } from 'lucide-react';

export default function PromptAssembler() {
  const { assembledPrompt, intents } = usePromptGateStore();
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (assembledPrompt) {
      navigator.clipboard.writeText(assembledPrompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
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
      {/* Header */}
      <div className="p-4 border-b border-dark-border flex items-center justify-between bg-brand-secondary/5">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-brand-secondary/20 rounded-md">
            <Sparkles size={18} className="text-brand-secondary" />
          </div>
          <h3 className="font-semibold text-text-primary">Optimized Prompt</h3>
        </div>
        <button 
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-brand-primary hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
          {copied ? <CheckCircle2 size={14} /> : <Copy size={14} />}
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>

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
      <div className="flex-1 p-5 overflow-y-auto">
        <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-[#A5B4FC]">
          {assembledPrompt}
        </pre>
      </div>

      {/* Footer Alert */}
      <div className="p-3 bg-brand-primary/10 border-t border-brand-primary/20 flex items-start gap-2 text-xs text-blue-200">
         <AlertCircle size={14} className="mt-0.5 shrink-0 text-brand-primary" />
         <p>PII 자동 마스킹 및 CoT(Chain of Thought) 최적화가 적용된 최종 프롬프트입니다. 즉시 사용 모델로 전송할 수 있습니다.</p>
      </div>
    </div>
  );
}
