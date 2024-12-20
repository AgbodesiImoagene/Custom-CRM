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
    integration_name: str,
    owner_email: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.register_crm_integration(
            integration_name, owner_email
        )
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


@router.get("/view_schema", response_model=schemas.SchemaResponse)
def view_schema(
    object_type: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.get_crm_integration()
        schema_fields = gong_service.list_schema_fields(integration_id, object_type)
        return {"schema_fields": schema_fields}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check_request_status", response_model=schemas.GongRequestStatusResponse)
def check_request_status(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.get_crm_integration()
        status, errors = gong_service.check_request_status(integration_id, request_id)
        return {"status": status, "errors": errors}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_crm_objects", response_model=schemas.CrmObjectsResponse)
def get_crm_objects(
    object_type: str,
    object_ids: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.get_crm_integration()
        object_ids_list = object_ids.split(",")
        objects = gong_service.get_crm_objects(
            integration_id, object_type, object_ids_list
        )
        return {"objects": objects}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_integration", response_model=schemas.MessageResponse)
def delete_integration(
    integration_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        gong_service.delete_crm_integration(integration_id)
        return {"message": "Integration deleted successfully."}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/view_integration_id", response_model=schemas.IntegrationResponse)
def view_integration_id(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin),
):
    gong_service = GongService(GONG_API_URL, credentials, BASE_URL, db)
    try:
        integration_id = gong_service.get_crm_integration()
        return {"integration_id": integration_id}
    except GongException as e:
        raise HTTPException(status_code=500, detail=str(e))
