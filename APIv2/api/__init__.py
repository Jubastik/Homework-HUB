from fastapi import APIRouter
from .student_api import router as student_router

router = APIRouter()
router.include_router(student_router)

