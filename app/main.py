from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, Base, get_db
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automação de Leads", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/leads", response_model=schemas.LeadOut)
def create_lead(payload: schemas.LeadCreate, db: Session = Depends(get_db)):
    lead = crud.create_lead(db, payload)
    lead = crud.apply_score_and_status(db, lead)

    # Example: here you could trigger async tasks, webhooks, or notify n8n via HTTP
    # For demo, we simply return the processed lead
    return lead

@app.get("/leads", response_model=list[schemas.LeadOut])
def list_leads(skip: int = 0, limit: int = 100, status: str | None = None, origem: str | None = None, db: Session = Depends(get_db)):
    return crud.list_leads(db, skip=skip, limit=limit, status=status, origem=origem)

@app.get("/leads/{lead_id}", response_model=schemas.LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = crud.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@app.put("/leads/{lead_id}", response_model=schemas.LeadOut)
def update_lead(lead_id: int, updates: schemas.LeadUpdate, db: Session = Depends(get_db)):
    lead = crud.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead = crud.update_lead(db, lead, updates)
    return lead

@app.post("/api/webhook/n8n")
def webhook_n8n(payload: dict, db: Session = Depends(get_db)):
    # n8n can POST incoming webhook payloads here.
    # The payload structure may vary; we'll store it as raw_payload and try to map common fields.
    data = {}
    # naive mapping
    data['nome'] = payload.get('nome') or payload.get('name') or payload.get('full_name')
    data['email'] = payload.get('email')
    data['telefone'] = payload.get('telefone') or payload.get('phone')
    data['origem'] = payload.get('origem') or payload.get('source') or 'n8n'
    data['interesse'] = payload.get('interesse') or payload.get('interest')
    data['renda_aproximada'] = payload.get('renda_aproximada') or payload.get('income')
    data['cidade'] = payload.get('cidade') or payload.get('city')

    lead_in = schemas.LeadCreate(**{**data, "raw_payload": payload})
    lead = crud.create_lead(db, lead_in)
    lead = crud.apply_score_and_status(db, lead)

    # In a real setup, you might call external services here (Slack, WhatsApp, CRM)
    return {"status": "ok", "id": lead.id, "calculated_status": lead.status, "score": lead.score}