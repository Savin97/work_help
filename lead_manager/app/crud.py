from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import date, timedelta
from . import models, schemas


# ── Leads ────────────────────────────────────────────────────────────────────

def get_leads(db: Session, status: str = None, industry: str = None, search: str = None):
    q = db.query(models.Lead)
    if status:
        q = q.filter(models.Lead.status == status)
    if industry:
        q = q.filter(models.Lead.industry == industry)
    if search:
        term = f"%{search}%"
        q = q.filter(or_(
            models.Lead.company.ilike(term),
            models.Lead.contact_name.ilike(term),
            models.Lead.email.ilike(term),
            models.Lead.equipment_interest.ilike(term),
        ))
    return q.order_by(models.Lead.company).all()


def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()


def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def update_lead(db: Session, lead_id: int, lead: schemas.LeadUpdate):
    db_lead = get_lead(db, lead_id)
    if not db_lead:
        return None
    for key, val in lead.model_dump(exclude_unset=True).items():
        setattr(db_lead, key, val)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def delete_lead(db: Session, lead_id: int):
    db_lead = get_lead(db, lead_id)
    if db_lead:
        db.delete(db_lead)
        db.commit()
    return db_lead


def get_dashboard_stats(db: Session):
    statuses = ["new", "contacted", "engaged", "proposal_sent", "won", "lost", "dormant"]
    counts = {}
    for s in statuses:
        counts[s] = db.query(models.Lead).filter(models.Lead.status == s).count()

    today = date.today()
    week_end = today + timedelta(days=7)
    overdue = db.query(models.Lead).filter(
        models.Lead.next_followup_date < today,
        ~models.Lead.status.in_(["won", "lost"])
    ).order_by(models.Lead.next_followup_date).all()
    due_this_week = db.query(models.Lead).filter(
        models.Lead.next_followup_date >= today,
        models.Lead.next_followup_date <= week_end,
        ~models.Lead.status.in_(["won", "lost"])
    ).order_by(models.Lead.next_followup_date).all()

    industry_counts = {}
    for row in db.query(models.Lead.industry, models.Lead.id).all():
        ind = row.industry or "other"
        industry_counts[ind] = industry_counts.get(ind, 0) + 1

    return {
        "status_counts": counts,
        "overdue": overdue,
        "due_this_week": due_this_week,
        "industry_counts": industry_counts,
        "total": sum(counts.values()),
    }


# ── Contact Logs ─────────────────────────────────────────────────────────────

def add_contact_log(db: Session, lead_id: int, log: schemas.ContactLogCreate):
    db_log = models.ContactLog(lead_id=lead_id, **log.model_dump())
    db.add(db_log)
    lead = get_lead(db, lead_id)
    if lead:
        lead.last_contact_date = log.date
        if log.next_followup_date:
            lead.next_followup_date = log.next_followup_date
        if lead.status == "new":
            lead.status = "contacted"
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_contact_log(db: Session, log_id: int):
    log = db.query(models.ContactLog).filter(models.ContactLog.id == log_id).first()
    if log:
        db.delete(log)
        db.commit()
    return log


# ── Bulk import ───────────────────────────────────────────────────────────────

def bulk_create_leads(db: Session, leads: list[schemas.LeadCreate]):
    created, skipped = 0, 0
    for lead_data in leads:
        existing = None
        if lead_data.email:
            existing = db.query(models.Lead).filter(
                models.Lead.email == lead_data.email
            ).first()
        if not existing and lead_data.company:
            existing = db.query(models.Lead).filter(
                models.Lead.company.ilike(lead_data.company)
            ).first()
        if existing:
            skipped += 1
        else:
            db.add(models.Lead(**lead_data.model_dump()))
            created += 1
    db.commit()
    return created, skipped
