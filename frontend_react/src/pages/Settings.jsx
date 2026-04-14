import React from 'react';

export default function Settings() {
  return (
    <div className="min-h-screen p-8 bg-dark-bg text-text-primary">
      <h1 className="text-3xl font-bold mb-6 text-brand-primary">Settings</h1>
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">API Key Configuration</h2>
        <p className="text-text-secondary mb-4">고급 모델 및 빠른 처리를 위한 본인만의 API 키를 입력하세요.</p>
        <div className="space-y-4 max-w-md">
           <div>
             <label className="block text-sm font-medium mb-1">OpenAI API Key</label>
             <input type="password" placeholder="sk-..." className="w-full bg-black/50 border border-dark-border rounded-lg p-2 text-text-primary outline-none focus:border-brand-primary transition-colors" />
           </div>
           <div>
             <label className="block text-sm font-medium mb-1">Anthropic API Key</label>
             <input type="password" placeholder="sk-ant-..." className="w-full bg-black/50 border border-dark-border rounded-lg p-2 text-text-primary outline-none focus:border-brand-primary transition-colors" />
           </div>
           <button className="bg-brand-primary hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors font-medium">Save Changes</button>
        </div>
      </div>
    </div>
  );
}
