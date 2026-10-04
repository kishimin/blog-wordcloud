from fastapi import APIRouter

from analysis.routes.image_by_entity import router as entity_image_router
from analysis.routes.image_by_frame_file import router as frame_file_image_router

router = APIRouter()
router.include_router(entity_image_router)
router.include_router(frame_file_image_router)
