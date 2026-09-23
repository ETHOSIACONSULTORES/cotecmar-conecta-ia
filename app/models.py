from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import relationship
from .db import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String(180), nullable=False)
    city = Column(String(120), nullable=False)
    venue = Column(String(180), nullable=True)
    event_date = Column(Date, nullable=True)
    public_code = Column(String(36), nullable=False, unique=True, index=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    providers = relationship("Provider", back_populates="event")

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    company_name = Column(String(180), nullable=False)
    contact_name = Column(String(160), nullable=False)
    contact_role = Column(String(160), nullable=True)
    phone = Column(String(80), nullable=False)
    email = Column(String(180), nullable=False, index=True)
    website = Column(String(300), nullable=True)
    linkedin = Column(String(300), nullable=True)
    city = Column(String(120), nullable=False)
    company_size = Column(String(80), nullable=False)
    portfolio_summary = Column(Text, nullable=False)
    document_name = Column(String(255), nullable=True)
    document_mime = Column(String(120), nullable=True)
    document_bytes = Column(LargeBinary, nullable=True)
    extracted_text = Column(Text, nullable=True)
    consent = Column(Boolean, default=False, nullable=False)
    consent_at = Column(DateTime, nullable=True)
    analysis_status = Column(String(40), default="pending", nullable=False)
    analysis_json = Column(Text, nullable=True)
    overall_score = Column(Integer, nullable=True)
    classification = Column(String(80), nullable=True)
    sector = Column(String(160), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    event = relationship("Event", back_populates="providers")

class Need(Base):
    __tablename__ = "needs"
    id = Column(Integer, primary_key=True)
    title = Column(String(220), nullable=False)
    category = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    source = Column(String(300), nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
