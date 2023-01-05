from fastapi import APIRouter
from .student_api import router as student_router
from .class_api import router as class_router
from .schedule_api import router as schedule_router
from .homework_api import router as homework_router

router = APIRouter()
router.include_router(student_router)
router.include_router(class_router)
router.include_router(schedule_router)
router.include_router(homework_router)
