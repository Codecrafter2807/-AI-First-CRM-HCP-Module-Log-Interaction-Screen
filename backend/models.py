from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    specialty = Column(String(255))
    location = Column(String(255))

    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    interaction_type = Column(String(255)) # e.g. Meeting, Call
    date = Column(DateTime, default=datetime.utcnow)
    attendees = Column(String(255))
    topics = Column(Text)
    materials_shared = Column(Text)
    samples_distributed = Column(Text)
    sentiment = Column(String(255)) # Positive, Neutral, Negative
    outcomes = Column(Text)
    summary = Column(Text)
    extracted_drugs = Column(Text)
    extracted_symptoms = Column(Text)
    extracted_specialties = Column(Text)
    follow_up_actions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hcp = relationship("HCP", back_populates="interactions")

class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    description = Column(String(255))
    due_date = Column(DateTime)
    status = Column(String(255), default="Pending")

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    type = Column(String(255)) # e.g. Brochure, Sample
