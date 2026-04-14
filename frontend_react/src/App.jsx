import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import Main from './pages/Main';
import History from './pages/History';
import Settings from './pages/Settings';
import { Network, History as HistoryIcon, Settings as SettingsIcon } from 'lucide-react';

function Navigation() {
  return (
    <nav className="h-16 border-b border-dark-border bg-dark-bg/80 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-50">
      <div className="flex items-center gap-3">
        <div className="bg-gradient-to-br from-brand-primary to-brand-secondary p-1.5 rounded-lg">
          <Network size={24} className="text-white" />
        </div>
        <span className="text-xl font-bold text-text-primary tracking-tight">PromptGate</span>
        <span className="px-2 py-0.5 rounded-full bg-brand-secondary/20 text-brand-secondary text-[10px] font-bold uppercase tracking-wider ml-1">Beta</span>
      </div>
      <div className="flex items-center gap-6">
        <NavLink 
          to="/" 
          className={({isActive}) => `text-sm font-medium transition-colors ${isActive ? 'text-brand-primary' : 'text-text-secondary hover:text-text-primary'}`}
        >
          Workspace
        </NavLink>
        <NavLink 
          to="/history" 
          className={({isActive}) => `flex items-center gap-1.5 text-sm font-medium transition-colors ${isActive ? 'text-brand-primary' : 'text-text-secondary hover:text-text-primary'}`}
        >
          <HistoryIcon size={16} /> History
        </NavLink>
        <NavLink 
          to="/settings" 
          className={({isActive}) => `flex items-center gap-1.5 text-sm font-medium transition-colors ${isActive ? 'text-brand-primary' : 'text-text-secondary hover:text-text-primary'}`}
        >
          <SettingsIcon size={16} /> Settings
        </NavLink>
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-dark-bg flex flex-col font-sans">
        <Navigation />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/history" element={<History />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
