from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api import schemas
from app.db import models
from app.api.security import get_current_active_user

router = APIRouter()


@router.post("/", response_model=schemas.Deal)
def create_deal(
    deal: schemas.DealCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    new_deal = models.Deal(**deal.model_dump())
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return new_deal


@router.get("/", response_model=list[schemas.Deal])
def read_deals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    deals = db.query(models.Deal).offset(skip).limit(limit).all()
    return deals


@router.get("/user/{user_id}", response_model=list[schemas.Deal])
def read_deals_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    deals = (
        db.query(models.Deal)
        .filter(models.Deal.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return deals


@router.get("/company/{company_id}", response_model=list[schemas.Deal])
def read_deals_by_company(
    company_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    deals = (
        db.query(models.Deal)
        .filter(models.Deal.company_id == company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return deals


@router.get("/stage/{stage}", response_model=list[schemas.Deal])
def read_deals_by_stage(
    stage: schemas.StageEnum,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    deals = (
        db.query(models.Deal)
        .filter(models.Deal.stage == stage)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return deals


@router.get("/status/{status}", response_model=list[schemas.Deal])
def read_deals_by_status(
    status: schemas.StatusEnum,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    deals = (
        db.query(models.Deal)
        .filter(models.Deal.status == status)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return deals


@router.get("/{deal_id}", response_model=schemas.Deal)
def read_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.put("/{deal_id}", response_model=schemas.Deal)
def update_deal(
    deal_id: int,
    deal: schemas.DealUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    if (
        current_user.id != db_deal.owner_id
        and current_user.role != schemas.RoleEnum.admin
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for key, value in deal.model_dump(exclude_unset=True).items():
        setattr(db_deal, key, value)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.delete("/{deal_id}", response_model=schemas.Deal)
def delete_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    if (
        current_user.id != db_deal.owner_id
        and current_user.role != schemas.RoleEnum.admin
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(db_deal)
    db.commit()
    return db_deal
