from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class InteractionBase(BaseModel):
    hcp_name: Optional[str] = None
    hcp_id: Optional[int] = None
    interaction_type: Optional[str] = None
    date: Optional[datetime] = None
    attendees: Optional[str] = None
    topics: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    summary: Optional[str] = None
    extracted_drugs: Optional[str] = None
    extracted_symptoms: Optional[str] = None
    extracted_specialties: Optional[str] = None
    follow_up_actions: Optional[str] = None

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class HCPBase(BaseModel):
    name: str
    specialty: str
    location: str

class HCP(HCPBase):
    id: int

    class Config:
        orm_mode = True
