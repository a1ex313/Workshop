from fastapi import APIRouter

from .auth import router as auth_router
from .operations import router as operations_router

print("init-api-1")


router = APIRouter()
router.include_router(auth_router)
router.include_router(operations_router)

print("init-api-2")