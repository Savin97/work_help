from pydantic import BaseModel
from typing import Optional
from datetime import date


class ContactLogCreate(BaseModel):
    date: date
    contact_type: str
    summary: Optional[str] = None
    outcome: Optional[str] = None
    next_followup_date: Optional[date] = None


class LeadCreate(BaseModel):
    company: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    industry: Optional[str] = None
    equipment_interest: Optional[str] = None
    status: Optional[str] = "new"
    source: Optional[str] = None
    notes: Optional[str] = None
    last_contact_date: Optional[date] = None
    next_followup_date: Optional[date] = None


class LeadUpdate(LeadCreate):
    pass
