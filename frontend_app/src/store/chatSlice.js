import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  messages: [
    { sender: 'ai', text: 'Hello! I am your AI Assistant. Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy...") or ask for help.' }
  ],
  isLoading: false
};

export const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    }
  }
});

export const { addMessage, setLoading } = chatSlice.actions;
export default chatSlice.reducer;
