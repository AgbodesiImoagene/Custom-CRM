from fastapi import APIRouter
from app.api.routes import companies, contacts, deals, leads, users, auth, gong
from app.services import gong_service

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(companies.router, prefix="/companies", tags=["companies"])
router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
router.include_router(deals.router, prefix="/deals", tags=["deals"])
router.include_router(leads.router, prefix="/leads", tags=["leads"])
router.include_router(gong.router, prefix="/gong", tags=["gong"])
