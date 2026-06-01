from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    phone = Column(String(100))
    email = Column(String(255))
    industry = Column(String(100))       # pharma | university | hospital | food | environmental | government | other
    equipment_interest = Column(Text)
    status = Column(String(50), default="new")  # new | contacted | engaged | proposal_sent | won | lost | dormant
    source = Column(String(255))         # exhibition name, referral, cold, etc.
    notes = Column(Text)
    last_contact_date = Column(Date)
    next_followup_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    contact_logs = relationship("ContactLog", back_populates="lead", cascade="all, delete-orphan", order_by="ContactLog.date.desc()")


class ContactLog(Base):
    __tablename__ = "contact_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    date = Column(Date, nullable=False)
    contact_type = Column(String(50))    # call | email | meeting | linkedin | other
    summary = Column(Text)
    outcome = Column(String(255))
    next_followup_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())

    lead = relationship("Lead", back_populates="contact_logs")
