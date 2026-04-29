import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  hcp_name: '',
  interaction_type: 'Meeting',
  date: new Date().toISOString().split('T')[0],
  time: new Date().toTimeString().slice(0,5),
  attendees: '',
  topics: '',
  materials_shared: '',
  samples_distributed: '',
  sentiment: 'Neutral',
  outcomes: '',
  summary: '',
  extracted_drugs: '',
  extracted_symptoms: '',
  extracted_specialties: '',
  follow_up_actions: ''
};

export const formSlice = createSlice({
  name: 'form',
  initialState,
  reducers: {
    updateField: (state, action) => {
      let { field, value } = action.payload;
      if (field === 'sentiment' && value) {
         value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
         if (!['Positive', 'Neutral', 'Negative'].includes(value)) return;
      }
      if (field in state) {
        state[field] = value;
      }
    },
    fillFromAI: (state, action) => {
      const data = action.payload;
      const appendFields = ['outcomes', 'topics', 'extracted_drugs', 'extracted_symptoms', 'extracted_specialties', 'follow_up_actions'];
      
      Object.keys(data).forEach(key => {
        let val = String(data[key]);
        if (val && !['null', 'none', 'unknown', 'undefined'].includes(val.toLowerCase())) {
          
          if (key === 'sentiment') {
             val = val.charAt(0).toUpperCase() + val.slice(1).toLowerCase();
             if (['Positive', 'Neutral', 'Negative'].includes(val)) state[key] = val;
          } else if (appendFields.includes(key) && state[key]) {
             const existing = state[key].toLowerCase();
             const newVal = val.toLowerCase();
             
             if (newVal.includes(existing)) {
               // New value is an expansion of the old one, so overwrite with the fuller version
               state[key] = val;
             } else if (!existing.includes(newVal)) {
               // New value is completely different, so append
               state[key] = `${state[key]}\n• ${val}`;
             }
          } else {
             state[key] = val;
          }
        }
      });
    },
    appendField: (state, action) => {
      const { field, value } = action.payload;
      if (field in state && value) {
        const val = String(value);
        if (!state[field]) {
          state[field] = val;
        } else {
          const existing = state[field].toLowerCase();
          const newVal = val.toLowerCase();
          if (newVal.includes(existing)) {
            state[field] = val;
          } else if (!existing.includes(newVal)) {
            state[field] = `${state[field]}\n• ${val}`;
          }
        }
      }
    },
    resetForm: () => initialState
  }
});

export const { updateField, fillFromAI, appendField, resetForm } = formSlice.actions;
export default formSlice.reducer;
