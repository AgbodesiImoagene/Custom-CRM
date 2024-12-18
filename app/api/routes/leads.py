from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api import schemas
from app.db import models
from app.api.security import get_current_active_user

router = APIRouter()


@router.post("/", response_model=schemas.Lead)
def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    new_lead = models.Lead(**lead.model_dump())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead


@router.get("/", response_model=list[schemas.Lead])
def read_leads(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    leads = db.query(models.Lead).offset(skip).limit(limit).all()
    return leads


@router.get("/user/{user_id}", response_model=list[schemas.Lead])
def read_leads_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    leads = (
        db.query(models.Lead)
        .filter(models.Lead.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return leads


@router.get("/status/{status}", response_model=list[schemas.Lead])
def read_leads_by_status(
    status: schemas.LeadStatusEnum,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    leads = (
        db.query(models.Lead)
        .filter(models.Lead.status == status)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return leads


@router.get("/{lead_id}", response_model=schemas.Lead)
def read_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}", response_model=schemas.Lead)
def update_lead(
    lead_id: int,
    lead: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    if (
        current_user.id != db_lead.owner_id
        and current_user.role != schemas.RoleEnum.admin
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for key, value in lead.model_dump(exclude_unset=True).items():
        setattr(db_lead, key, value)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@router.delete("/{lead_id}", response_model=schemas.Lead)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    if (
        current_user.id != db_lead.owner_id
        and current_user.role != schemas.RoleEnum.admin
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(db_lead)
    db.commit()
    return db_lead
