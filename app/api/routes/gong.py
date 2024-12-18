from fastapi import APIRouter, HTTPException, Depends
from app.services.gong_service import GongService, GongException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.security import get_current_active_admin
from app.api import schemas
import os

router = APIRouter()

GONG_API_URL = os.getenv("GONG_API_URL")
GONG_ACCESS_KEY = os.getenv("GONG_ACCESS_KEY")
GONG_ACCESS_KEY_SECRET = os.getenv("GONG_ACCESS_KEY_SECRET")
credentials = (GONG_ACCESS_KEY, GONG_ACCESS_KEY_SECRET)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@router.post("/register_integration", response_model=schemas.IntegrationResponse)
def register_integration(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.register_crm_integration()
        return {"integration_id": integration_id}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update_schema", response_model=schemas.MessageResponse)
def update_schema(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.get_crm_integration()
        gong_service.register_crm_schema(integration_id)
        return {"message": "Schema updated successfully."}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/full_db_dump", response_model=schemas.MessageResponse)
def full_db_dump(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.get_crm_integration()
        users, companies, contacts, deals, leads = gong_service.fetch_data_from_db()
        gong_service.push_users_to_gong(integration_id, users)
        gong_service.push_companies_to_gong(integration_id, companies)
        gong_service.push_contacts_to_gong(integration_id, contacts)
        gong_service.push_deals_to_gong(integration_id, deals)
        gong_service.push_leads_to_gong(integration_id, leads)
        return {"message": "Full database dump completed successfully."}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))
