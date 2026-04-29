import LogInteractionForm from './components/LogInteractionForm';
import AIAssistant from './components/AIAssistant';
import { Activity } from 'lucide-react';

function App() {
  return (
    <div className="app-container">
      <div style={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
        <div className="header-area">
          <div className="header-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity color="#2563eb" />
            AI-First CRM HCP Module
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginTop: '4px' }}>
            Log interactions manually or use the LangGraph AI Assistant to auto-fill the form.
          </p>
        </div>
        
        <div className="main-content">
          <LogInteractionForm />
          <AIAssistant />
        </div>
      </div>
    </div>
  );
}

export default App;
