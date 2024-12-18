from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api import schemas
from app.db import models
from app.api.security import get_current_active_user

router = APIRouter()


@router.post("/", response_model=schemas.Company)
def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_company = (
        db.query(models.Company).filter(models.Company.name == company.name).first()
    )
    if db_company:
        raise HTTPException(status_code=400, detail="Company name already exists")

    new_company = models.Company(
        name=company.name,
        industry=company.industry,
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    for domain in company.domains:
        new_domain = models.Domain(name=domain.name, company_id=new_company.id)
        db.add(new_domain)

    db.commit()
    db.refresh(new_company)
    return new_company


@router.get("/", response_model=list[schemas.Company])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    companies = db.query(models.Company).offset(skip).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=schemas.Company)
def read_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/industry/{industry}", response_model=list[schemas.Company])
def read_companies_by_industry(
    industry: schemas.IndustryEnum,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    companies = (
        db.query(models.Company)
        .filter(models.Company.industry == industry)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return companies


@router.put("/{company_id}", response_model=schemas.Company)
def update_company(
    company_id: int,
    company: schemas.CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_company = (
        db.query(models.Company).filter(models.Company.id == company_id).first()
    )
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in company.model_dump(exclude_unset=True).items():
        if key == "domains":
            # Clear existing domains
            db.query(models.Domain).filter(
                models.Domain.company_id == company_id
            ).delete()
            # Add new domains
            for domain in value:
                new_domain = models.Domain(name=domain.name, company_id=company_id)
                db.add(new_domain)
        else:
            setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company


@router.delete("/{company_id}", response_model=schemas.Company)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return company
