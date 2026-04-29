from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import models, schemas
from database import engine, get_db
from agent import app as langgraph_app
from langchain_core.messages import HumanMessage, AIMessage
import json

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM HCP Module")

# Configure CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify the exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-First CRM API"}

@app.post("/api/chat")
def chat(request_data: Dict[str, Any]):
    """
    Main endpoint for the LangGraph agent.
    Takes the current message and history, runs the LangGraph workflow.
    """
    user_message = request_data.get("message")
    history = request_data.get("history", []) # Get the chat history from frontend
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Reconstruct the message list for LangGraph
    messages = []
    for msg in history:
        if msg["sender"] == "user":
            messages.append(HumanMessage(content=msg["text"]))
        elif msg["sender"] == "ai" and not msg.get("isSystem"):
            messages.append(AIMessage(content=msg["text"]))
            
    # Add the latest user message
    messages.append(HumanMessage(content=user_message))

    # Run the LangGraph agent with full context
    try:
        final_state = langgraph_app.invoke({"messages": messages})
    except Exception as e:
        print(f"Agent Error: {str(e)}")
        return {"response": f"Error communicating with AI: {str(e)}", "tool_data": []}

    # Extract the final response text
    final_messages = final_state["messages"]
    ai_response = final_messages[-1].content if final_messages else "No response generated."

    # Extract only the NEW tool output from this specific turn
    tool_data = []
    # Find the index of the last user message to only pick up tools from THIS turn
    last_user_msg_index = -1
    for i in range(len(final_messages) - 1, -1, -1):
        if isinstance(final_messages[i], HumanMessage):
            last_user_msg_index = i
            break
            
    # Collect tool messages that appeared after the current user message
    if last_user_msg_index != -1:
        for msg in final_messages[last_user_msg_index+1:]:
            if msg.type == "tool":
                try:
                    data = json.loads(msg.content)
                    tool_data.append(data)
                except:
                    pass

    return {
        "response": ai_response,
        "tool_data": tool_data 
    }

@app.post("/log-interaction", response_model=schemas.Interaction)
def log_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    """
    Direct endpoint to save the structured form payload to the DB.
    """
    # 1. Handle HCP Lookup/Creation
    hcp_id = interaction.hcp_id
    if not hcp_id and interaction.hcp_name:
        # Find existing HCP by name or create a new one
        db_hcp = db.query(models.HCP).filter(models.HCP.name == interaction.hcp_name).first()
        if not db_hcp:
            db_hcp = models.HCP(name=interaction.hcp_name, specialty="Unknown", location="Unknown")
            db.add(db_hcp)
            db.commit()
            db.refresh(db_hcp)
        hcp_id = db_hcp.id
    
    # 2. Create the interaction
    interaction_data = interaction.dict(exclude={"hcp_name"})
    interaction_data["hcp_id"] = hcp_id
    
    db_interaction = models.Interaction(**interaction_data)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@app.put("/edit-interaction/{interaction_id}", response_model=schemas.Interaction)
def edit_interaction(interaction_id: int, interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    db_interaction = db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    update_data = interaction.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_interaction, key, value)
        
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@app.get("/get-hcp", response_model=List[schemas.HCP])
def get_hcps(db: Session = Depends(get_db)):
    """
    Retrieves the list of available HCPs.
    """
    hcps = db.query(models.HCP).all()
    # Seed mock data if empty
    if not hcps:
        mock_hcps = [
            models.HCP(name="Dr. Smith", specialty="Cardiology", location="NY"),
            models.HCP(name="Dr. Sharma", specialty="Endocrinology", location="SF"),
            models.HCP(name="Dr. Mehta", specialty="Oncology", location="Boston")
        ]
        db.add_all(mock_hcps)
        db.commit()
        hcps = db.query(models.HCP).all()
    return hcps

@app.post("/suggest-followup")
def suggest_followup(context: Dict[str, str]):
    """
    Explicit call for follow-up suggestions (can be used directly from UI).
    """
    # In a full implementation, this could invoke a specific LLM chain.
    # For now, it returns a mock based on the context.
    return {"suggestions": ["Schedule next meeting", "Send brochure"]}
