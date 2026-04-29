import { useSelector, useDispatch } from 'react-redux';
import { updateField, resetForm } from '../store/formSlice';
import { Calendar, Save, FileText, Search } from 'lucide-react';
import axios from 'axios';

export default function LogInteractionForm() {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.form);

  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateField({ field: name, value }));
  };

  const handleSave = async () => {
    try {
      console.log("Saving interaction to DB:", formData);
      const response = await axios.post('http://localhost:8000/log-interaction', formData);
      console.log("Save successful:", response.data);
      alert("✅ Interaction successfully saved to MySQL database (assesment)!");
    } catch (error) {
      console.error("Save error:", error);
      alert("❌ Failed to save interaction. Check backend console.");
    }
  };

  return (
    <div className="form-panel">
      <div className="panel-header">
        <FileText size={24} />
        Log HCP Interaction
      </div>
      
      <div className="form-grid">
        <div className="form-group full-width">
          <label>HCP Name</label>
          <div style={{ position: 'relative' }}>
            <input 
              type="text" 
              name="hcp_name"
              placeholder="Search or select HCP..." 
              value={formData.hcp_name || ''}
              onChange={handleChange}
            />
            <Search size={16} style={{ position: 'absolute', right: 12, top: 12, color: '#94a3b8' }} />
          </div>
        </div>

        <div className="form-group">
          <label>Interaction Type</label>
          <select name="interaction_type" value={formData.interaction_type} onChange={handleChange}>
            <option>Meeting</option>
            <option>Call</option>
            <option>Email</option>
          </select>
        </div>

        <div className="form-group">
          <label>Date</label>
          <div style={{ position: 'relative' }}>
            <input 
              type="date" 
              name="date"
              value={formData.date}
              onChange={handleChange}
            />
            <Calendar size={16} style={{ position: 'absolute', right: 12, top: 12, color: '#94a3b8', pointerEvents: 'none' }} />
          </div>
        </div>

        <div className="form-group full-width">
          <label>Topics Discussed</label>
          <textarea 
            name="topics"
            placeholder="Enter key discussion points..."
            value={formData.topics || ''}
            onChange={handleChange}
          ></textarea>
        </div>

        <div className="form-group full-width">
          <label>Professional Summary</label>
          <textarea 
            name="summary"
            placeholder="AI-generated professional summary..."
            value={formData.summary || ''}
            onChange={handleChange}
            style={{ minHeight: '100px', backgroundColor: '#f8fafc' }}
          ></textarea>
        </div>

        <div className="form-group full-width">
          <label className="section-subtitle">Medical Insights (AI-Extracted)</label>
          <div className="medical-insights-grid">
            <div className="form-group">
              <label>Drugs Mentioned</label>
              <input 
                type="text" 
                name="extracted_drugs" 
                value={formData.extracted_drugs || ''} 
                onChange={handleChange}
                placeholder="e.g. OncoBoost"
                className="medical-input"
              />
            </div>
            <div className="form-group">
              <label>Symptoms/Conditions</label>
              <input 
                type="text" 
                name="extracted_symptoms" 
                value={formData.extracted_symptoms || ''} 
                onChange={handleChange}
                placeholder="e.g. Fatigue"
                className="medical-input"
              />
            </div>
            <div className="form-group">
              <label>Specialties</label>
              <input 
                type="text" 
                name="extracted_specialties" 
                value={formData.extracted_specialties || ''} 
                onChange={handleChange}
                placeholder="e.g. Oncology"
                className="medical-input"
              />
            </div>
          </div>
        </div>

        <div className="form-group full-width">
          <label>Materials Shared</label>
          <input 
            type="text" 
            name="materials_shared"
            placeholder="Enter materials shared..."
            value={formData.materials_shared || ''}
            onChange={handleChange}
          />
        </div>

        <div className="form-group full-width">
          <label>Observed/Inferred HCP Sentiment</label>
          <div className="radio-group">
            <label className="radio-label">
              <input 
                type="radio" 
                name="sentiment" 
                value="Positive"
                checked={formData.sentiment === 'Positive'}
                onChange={handleChange}
              />
              Positive
            </label>
            <label className="radio-label">
              <input 
                type="radio" 
                name="sentiment" 
                value="Neutral"
                checked={formData.sentiment === 'Neutral'}
                onChange={handleChange}
              />
              Neutral
            </label>
            <label className="radio-label">
              <input 
                type="radio" 
                name="sentiment" 
                value="Negative"
                checked={formData.sentiment === 'Negative'}
                onChange={handleChange}
              />
              Negative
            </label>
          </div>
        </div>

        <div className="form-group full-width">
          <label>Outcomes</label>
          <textarea 
            name="outcomes"
            placeholder="Key outcomes or agreements..."
            value={formData.outcomes || ''}
            onChange={handleChange}
          ></textarea>
        </div>
        
        <div className="form-group full-width">
          <label>Follow-up Actions</label>
          <textarea 
            name="follow_up_actions"
            placeholder="Enter next steps or tasks..."
            value={formData.follow_up_actions || ''}
            onChange={handleChange}
          ></textarea>
        </div>
      </div>
      
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '24px' }}>
        <button className="btn btn-secondary" onClick={() => dispatch(resetForm())} style={{ backgroundColor: '#f1f5f9', color: '#475569' }}>
          Reset
        </button>
        <button className="btn btn-primary" onClick={handleSave}>
          <Save size={16} /> Save Interaction
        </button>
      </div>
    </div>
  );
}
