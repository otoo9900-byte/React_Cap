import React, { useState, useRef, useEffect } from 'react';
import usePromptGateStore from '../../store/usePromptGateStore';
import { Send, Bot, User, Loader2 } from 'lucide-react';

export default function ChatInterface() {
  const { messages, isTyping, sendMessageMock } = usePromptGateStore();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessageMock(input.trim());
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-dark-card border-r border-dark-border shadow-xl">
      {/* Header */}
      <div className="p-4 border-b border-dark-border flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-brand-primary/20 flex items-center justify-center text-brand-primary">
          <Bot size={20} />
        </div>
        <div>
          <h2 className="font-semibold text-text-primary text-lg">Agentic Interviewer</h2>
          <p className="text-xs text-text-secondary">AI와 대화하며 최적의 프롬프트를 완성하세요</p>
        </div>
      </div>

      {/* Message List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-brand-secondary/20 text-brand-secondary' : 'bg-brand-primary/20 text-brand-primary'}`}>
              {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
            </div>
            <div className={`max-w-[80%] rounded-2xl p-3 ${msg.role === 'user' ? 'bg-brand-secondary/10 border border-brand-secondary/20 text-text-primary rounded-tr-none' : 'bg-[#1A1A1A] border border-dark-border text-text-primary rounded-tl-none'}`}>
              <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-brand-primary/20 flex items-center justify-center shrink-0 text-brand-primary">
              <Bot size={18} />
            </div>
            <div className="max-w-[80%] rounded-2xl p-4 bg-[#1A1A1A] border border-dark-border rounded-tl-none flex items-center gap-2">
              <Loader2 size={16} className="animate-spin text-brand-primary" />
              <span className="text-xs text-text-secondary">분석 중...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-dark-bg/50 border-t border-dark-border">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="프롬프트 목적을 입력하세요..."
            className="w-full bg-[#1A1A1A] border border-dark-border rounded-full pl-4 pr-12 py-3 text-text-primary text-sm outline-none focus:border-brand-secondary transition-colors placeholder:text-text-secondary"
            disabled={isTyping}
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="absolute right-2 p-2 bg-brand-secondary hover:bg-violet-600 disabled:opacity-50 disabled:hover:bg-brand-secondary text-white rounded-full transition-colors flex items-center justify-center"
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  );
}
