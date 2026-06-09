import React, { useState, useEffect } from 'react';
import usePromptGateStore from '../../store/usePromptGateStore';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, CheckCircle2, Sparkles, AlertCircle, Calendar, Terminal, Loader2, ArrowRight } from 'lucide-react';

const INTENT_LABELS = {
  destination: '목적지 📍',
  budget: '예산 💵',
  duration: '기간 📅',
  companion: '동반자 👥',
  style: '여행 스타일 ✨',
  food_preference: '음식 취향 🍕'
};

// Custom components to style Markdown elements with premium dark aesthetics
const markdownComponents = {
  table: ({ node, ...props }) => (
    <div className="overflow-x-auto my-4 rounded-xl border border-dark-border shadow-md">
      <table className="w-full text-left border-collapse text-sm text-text-primary" {...props} />
    </div>
  ),
  thead: ({ node, ...props }) => (
    <thead className="bg-brand-primary/10 border-b border-dark-border text-xs uppercase tracking-wider text-brand-primary" {...props} />
  ),
  tbody: ({ node, ...props }) => (
    <tbody className="divide-y divide-dark-border bg-[#121212]" {...props} />
  ),
  tr: ({ node, ...props }) => (
    <tr className="hover:bg-dark-border/30 transition-colors" {...props} />
  ),
  th: ({ node, ...props }) => (
    <th className="px-4 py-3 font-semibold text-text-primary" {...props} />
  ),
  td: ({ node, ...props }) => (
    <td className="px-4 py-3 text-[#E2E8F0] leading-relaxed" {...props} />
  ),
  h1: ({ node, ...props }) => <h1 className="text-xl font-bold text-text-primary mt-6 mb-3 border-b border-dark-border pb-1" {...props} />,
  h2: ({ node, ...props }) => <h2 className="text-lg font-semibold text-text-primary mt-5 mb-2" {...props} />,
  h3: ({ node, ...props }) => <h3 className="text-base font-medium text-text-primary mt-4 mb-2" {...props} />,
  p: ({ node, ...props }) => <p className="text-[#94A3B8] leading-relaxed my-2" {...props} />,
  ul: ({ node, ...props }) => <ul className="list-disc list-inside my-2 space-y-1 text-[#94A3B8]" {...props} />,
  ol: ({ node, ...props }) => <ol className="list-decimal list-inside my-2 space-y-1 text-[#94A3B8]" {...props} />,
  li: ({ node, ...props }) => <li className="leading-relaxed" {...props} />,
  strong: ({ node, ...props }) => <strong className="text-brand-secondary font-semibold" {...props} />,
};

export default function PromptAssembler() {
  const { assembledPrompt, travelPlan, intents } = usePromptGateStore();
  const [activeTab, setActiveTab] = useState('prompt');
  const [copied, setCopied] = useState(false);
  const [loadingItinerary, setLoadingItinerary] = useState(false);

  // Keep tab defaulted to 'prompt' when a new session starts
  useEffect(() => {
    if (!assembledPrompt) {
      setActiveTab('prompt');
    }
  }, [assembledPrompt]);

  const handleCopy = () => {
    const textToCopy = activeTab === 'prompt' ? assembledPrompt : travelPlan;
    if (textToCopy) {
      navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleLoadItinerary = () => {
    if (!travelPlan) return;
    setLoadingItinerary(true);
    // Smooth loading experience for user satisfaction
    setTimeout(() => {
      setLoadingItinerary(false);
      setActiveTab('itinerary');
    }, 1200);
  };

  if (!assembledPrompt) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center bg-dark-card rounded-2xl border border-dark-border shadow-lg">
        <Sparkles size={48} className="text-brand-secondary/30 mb-4" />
        <h3 className="text-lg font-medium text-text-secondary mb-2">프롬프트 조립 대기 중</h3>
        <p className="text-sm text-text-secondary w-2/3">좌측 채팅에서 AI와 대화를 완료하면 이곳에 전문가 수준의 프롬프트와 상세 일정이 완성됩니다.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-dark-card rounded-2xl border border-brand-secondary/30 shadow-[0_0_30px_rgba(139,92,246,0.1)] relative overflow-hidden">
      {/* Header & Tabs */}
      <div className="border-b border-dark-border bg-brand-secondary/5 flex flex-col sm:flex-row sm:items-center justify-between p-2 gap-2">
        <div className="flex gap-1 p-1 bg-dark-bg rounded-xl border border-dark-border">
          <button
            onClick={() => setActiveTab('prompt')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'prompt'
                ? 'bg-brand-secondary text-white shadow-md'
                : 'text-text-secondary hover:text-text-primary hover:bg-dark-card/50'
            }`}
          >
            <Terminal size={14} />
            Optimized Prompt
          </button>
          
          {travelPlan && (
            <button
              onClick={() => setActiveTab('itinerary')}
              className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
                activeTab === 'itinerary'
                  ? 'bg-brand-primary text-white shadow-md'
                  : 'text-text-secondary hover:text-text-primary hover:bg-dark-card/50'
              }`}
            >
              <Calendar size={14} />
              Travel Itinerary
            </button>
          )}
        </div>

        <button 
          onClick={handleCopy}
          className="flex items-center justify-center gap-1.5 px-4 py-2 text-xs font-semibold bg-brand-primary hover:bg-blue-600 text-white rounded-lg transition-colors shrink-0"
        >
          {copied ? <CheckCircle2 size={14} /> : <Copy size={14} />}
          {copied ? 'Copied' : 'Copy Content'}
        </button>
      </div>

      {/* Intents Meta */}
      {intents && (
         <div className="px-5 pt-4 pb-2 flex flex-wrap gap-2 border-b border-dark-border/30 bg-[#121212]/50">
            {Object.entries(intents).map(([key, value]) => (
               value && (
                 <div key={key} className="px-2.5 py-1 text-xs bg-dark-border text-text-secondary rounded-md border border-[#333]">
                   <span className="font-medium">{INTENT_LABELS[key] || key}</span>: <span className="text-text-primary ml-1">{value}</span>
                 </div>
               )
            ))}
         </div>
      )}

      {/* Content Area */}
      <div className="flex-1 p-5 overflow-y-auto flex flex-col justify-between">
        {activeTab === 'prompt' ? (
          <div className="flex-1 flex flex-col justify-between">
            <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-[#A5B4FC] mb-6">
              {assembledPrompt}
            </pre>
            
            {travelPlan && (
              <div className="mt-auto pt-6 border-t border-dark-border/50 flex flex-col items-center p-4 bg-brand-secondary/5 rounded-xl border border-brand-secondary/20">
                <p className="text-xs text-text-secondary mb-3 text-center">
                  슬롯 분석이 완료되고 맞춤 일정이 백엔드에 준비되었습니다. 아래 버튼을 눌러 상세 일정을 불러오세요.
                </p>
                <button
                  onClick={handleLoadItinerary}
                  disabled={loadingItinerary}
                  className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-brand-secondary to-brand-primary hover:from-purple-600 hover:to-blue-600 text-white font-semibold text-sm rounded-xl shadow-lg hover:shadow-purple-500/20 transition-all disabled:opacity-50"
                >
                  {loadingItinerary ? (
                    <>
                      <Loader2 size={16} className="animate-spin" />
                      일정표 구성 중...
                    </>
                  ) : (
                    <>
                      <Calendar size={16} />
                      최종 일정표 불러오기
                      <ArrowRight size={14} />
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="prose prose-invert max-w-none text-sm">
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
              {travelPlan}
            </ReactMarkdown>
          </div>
        )}
      </div>

      {/* Footer Alert */}
      <div className="p-3 bg-brand-primary/10 border-t border-brand-primary/20 flex items-start gap-2 text-xs text-blue-200">
         <AlertCircle size={14} className="mt-0.5 shrink-0 text-brand-primary" />
         <p>
           {activeTab === 'prompt' 
             ? 'PII 자동 마스킹 및 CoT(Chain of Thought) 최적화가 적용된 최종 프롬프트입니다.'
             : '사용자의 선호도와 엄격한 동선 제약이 반영된 맞춤형 추천 일정표입니다.'}
         </p>
      </div>
    </div>
  );
}
