import React, { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addMessage, setLoading } from '../store/chatSlice';
import { fillFromAI, updateField, appendField } from '../store/formSlice';
import { Bot, Send, User } from 'lucide-react';
import axios from 'axios';

export default function AIAssistant() {
  const [input, setInput] = useState('');
  const chatState = useSelector((state) => state.chat);
  const dispatch = useDispatch();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    dispatch(addMessage({ sender: 'user', text: userMessage }));
    setInput('');
    dispatch(setLoading(true));

    try {
      // Send to FastAPI backend with full chat history
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: userMessage,
        history: chatState.messages
      });

      const data = response.data;

      // Add AI response to chat
      if (data.response) {
        dispatch(addMessage({ sender: 'ai', text: data.response }));
      }

      // Process any tool data returned by LangGraph to update the form
      if (data.tool_data && data.tool_data.length > 0) {
        data.tool_data.forEach(toolAction => {
          if (toolAction.action === 'LOG_INTERACTION') {
            dispatch(fillFromAI(toolAction.data));
            dispatch(addMessage({ sender: 'ai', text: '✅ Form updated with extracted details.', isSystem: true }));
          } else if (toolAction.action === 'EDIT_INTERACTION') {
            dispatch(updateField({ field: toolAction.data.field, value: toolAction.data.value }));
            dispatch(addMessage({ sender: 'ai', text: `✅ Updated ${toolAction.data.field}.`, isSystem: true }));
          } else if (toolAction.action === 'SUMMARIZE_NOTES') {
            dispatch(updateField({ field: 'summary', value: toolAction.data.summary || toolAction.data.raw_notes }));
            dispatch(addMessage({ sender: 'ai', text: '✅ Professional summary generated.', isSystem: true }));
          } else if (toolAction.action === 'EXTRACT_ENTITIES') {
            const { drug_names, symptoms, specialties } = toolAction.data;
            let entityText = '🔍 **Extracted Entities:**\n';
            if (drug_names?.length) entityText += `• **Drugs:** ${drug_names.join(', ')}\n`;
            if (symptoms?.length) entityText += `• **Symptoms:** ${symptoms.join(', ')}\n`;
            if (specialties?.length) entityText += `• **Specialties:** ${specialties.join(', ')}`;
            
            // Update form fields for medical insights
            if (drug_names?.length) drug_names.forEach(drug => dispatch(appendField({ field: 'extracted_drugs', value: drug })));
            if (symptoms?.length) symptoms.forEach(symptom => dispatch(appendField({ field: 'extracted_symptoms', value: symptom })));
            if (specialties?.length) specialties.forEach(specialty => dispatch(appendField({ field: 'extracted_specialties', value: specialty })));

            dispatch(addMessage({ sender: 'ai', text: entityText, isSystem: true }));
          } else if (toolAction.action === 'RECOMMEND_FOLLOWUP') {
            dispatch(appendField({ field: 'follow_up_actions', value: toolAction.data.recommendation }));
            dispatch(addMessage({ sender: 'ai', text: '✅ Added follow-up recommendation.', isSystem: true }));
          }
        });
      }

    } catch (error) {
      console.error("Chat error:", error);
      dispatch(addMessage({ sender: 'ai', text: 'Sorry, I encountered an error communicating with the backend.' }));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="ai-panel">
      <div className="ai-header">
        <Bot size={20} color="#2563eb" />
        <h3>AI Assistant</h3>
        <span className="glass-badge">LangGraph Powered</span>
      </div>

      <div className="chat-history">
        {chatState.messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender} ${msg.isSystem ? 'system-msg' : ''}`}>
            {msg.text}
          </div>
        ))}
        {chatState.isLoading && (
          <div className="typing-indicator">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="input-wrapper">
          <input
            type="text"
            placeholder="Describe interaction..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={chatState.isLoading}
          />
          <button 
            className="send-btn" 
            onClick={handleSend}
            disabled={!input.trim() || chatState.isLoading}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
