from sqlalchemy.orm import Session
from app import models, schemas
import json

def create_lead(db: Session, lead_in: schemas.LeadCreate):
    lead = models.Lead(
        nome=lead_in.nome,
        email=lead_in.email,
        telefone=lead_in.telefone,
        origem=lead_in.origem,
        interesse=lead_in.interesse,
        renda_aproximada=lead_in.renda_aproximada,
        cidade=lead_in.cidade,
        raw_payload=json.dumps(lead_in.raw_payload) if lead_in.raw_payload else None
    )
    db.add(lead)
    db.flush()
    db.refresh(lead)
    return lead

def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()

def list_leads(db: Session, skip: int = 0, limit: int = 100, status: str = None, origem: str = None):
    q = db.query(models.Lead)
    if status:
        q = q.filter(models.Lead.status == status)
    if origem:
        q = q.filter(models.Lead.origem == origem)
    return q.order_by(models.Lead.created_at.desc()).offset(skip).limit(limit).all()

def update_lead(db: Session, lead: models.Lead, updates: schemas.LeadUpdate):
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(lead, key, value)
    db.add(lead)
    db.flush()
    db.refresh(lead)
    return lead

def apply_score_and_status(db: Session, lead: models.Lead):
    # Scoring rules - simple example, customize as needed
    score = 0
    if lead.email:
        score += 10
    if lead.telefone:
        score += 10
    if lead.renda_aproximada and lead.renda_aproximada > 7000:
        score += 15
    if lead.interesse and any(k.lower() in lead.interesse.lower() for k in ['imóvel', 'imovel', 'casa', 'apartamento']):
        score += 10
    if lead.cidade and lead.cidade.lower() in ['são paulo', 'saopaulo', 'sao paulo']:
        score += 5

    lead.score = score
    if score >= 30:
        lead.status = 'quente'
    elif score >= 15:
        lead.status = 'morno'
    else:
        lead.status = 'frio'

    db.add(lead)
    db.flush()
    db.refresh(lead)
    return lead