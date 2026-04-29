from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import json
from datetime import datetime

# 1. Log Interaction Tool (MANDATORY)
class LogInteractionInput(BaseModel):
    hcp_name: Optional[str] = Field(description="Name of the Healthcare Professional (HCP)")
    topics: Optional[str] = Field(description="Topics discussed during the interaction")
    sentiment: Optional[str] = Field(description="Observed sentiment: Positive, Neutral, or Negative")
    outcomes: Optional[str] = Field(description="Key outcomes or agreements")
    materials_shared: Optional[str] = Field(description="Any materials or samples shared")
    drug_names: Optional[List[str]] = Field(description="List of drug names mentioned", default=[])
    symptoms: Optional[List[str]] = Field(description="List of symptoms or conditions mentioned", default=[])
    concerns: Optional[str] = Field(description="Any concerns raised by the HCP, optional", default=None)
    notes: Optional[str] = Field(description="Any extra notes", default=None)

@tool("log_interaction", args_schema=LogInteractionInput)
def log_interaction(hcp_name: Optional[str] = None, topics: Optional[str] = None, sentiment: Optional[str] = None, outcomes: Optional[str] = None, materials_shared: Optional[str] = None, drug_names: Optional[List[str]] = [], symptoms: Optional[List[str]] = [], concerns: Optional[str] = None, notes: Optional[str] = None) -> str:
    """
    Logs a new interaction with an HCP and extracts structured fields from the conversation.
    Use this tool when the user provides details about a recent meeting or call to save it.
    """
    # In a real app, this would save to DB. For the agent response, we return the structured data.
    # The frontend will use this structured data to update the UI form state.
    interaction_data = {
        "action": "LOG_INTERACTION",
        "data": {
            "hcp_name": hcp_name,
            "topics": topics,
            "sentiment": sentiment,
            "outcomes": outcomes,
            "materials_shared": materials_shared,
            "extracted_drugs": drug_names if isinstance(drug_names, str) else ", ".join(drug_names) if drug_names else "",
            "extracted_symptoms": symptoms if isinstance(symptoms, str) else ", ".join(symptoms) if symptoms else ""
        }
    }
    return json.dumps(interaction_data)

# 2. Edit Interaction Tool (MANDATORY)
class EditInteractionInput(BaseModel):
    field_to_edit: str = Field(description="The field to modify, e.g., 'sentiment', 'topics', 'outcomes'")
    new_value: str = Field(description="The new value for the field")

@tool("edit_interaction", args_schema=EditInteractionInput)
def edit_interaction(field_to_edit: str, new_value: str) -> str:
    """
    Modifies an existing interaction record. 
    Use this when the user says something like 'Change sentiment to negative' or 'Add XYZ to topics'.
    """
    edit_data = {
        "action": "EDIT_INTERACTION",
        "data": {
            "field": field_to_edit,
            "value": new_value
        }
    }
    return json.dumps(edit_data)

# 3. Summarization Tool
class SummarizationInput(BaseModel):
    summary: str = Field(description="The clean, professional summary of the raw notes")

@tool("summarize_notes", args_schema=SummarizationInput)
def summarize_notes(summary: str) -> str:
    """
    Use this tool when asked to summarize long or rough notes. Pass the generated professional summary here.
    """
    summary_data = {
        "action": "SUMMARIZE_NOTES",
        "data": {
            "summary": summary
        }
    }
    return json.dumps(summary_data)

# 4. Follow-up Recommendation Tool
class FollowUpInput(BaseModel):
    recommendation: str = Field(description="The specific follow-up actions recommended based on the conversation")

@tool("recommend_followup", args_schema=FollowUpInput)
def recommend_followup(recommendation: str) -> str:
    """
    Suggests next steps (e.g., scheduling next meeting, sending brochure).
    """
    follow_up_data = {
        "action": "RECOMMEND_FOLLOWUP",
        "data": {
            "recommendation": recommendation
        }
    }
    return json.dumps(follow_up_data)

# 5. Entity Extraction Tool
class EntityExtractionInput(BaseModel):
    drug_names: List[str] = Field(description="List of drug names mentioned")
    symptoms: List[str] = Field(description="List of symptoms or conditions mentioned")
    specialties: List[str] = Field(description="List of HCP specialties mentioned")

@tool("extract_entities", args_schema=EntityExtractionInput)
def extract_entities(drug_names: List[str], symptoms: List[str], specialties: List[str]) -> str:
    """
    Extracts specific domain entities like Drug Names, HCP Specialties, or Symptoms.
    """
    entity_data = {
        "action": "EXTRACT_ENTITIES",
        "data": {
            "drug_names": drug_names,
            "symptoms": symptoms,
            "specialties": specialties
        }
    }
    return json.dumps(entity_data)

# List of all tools
TOOLS = [log_interaction, edit_interaction, summarize_notes, recommend_followup, extract_entities]
