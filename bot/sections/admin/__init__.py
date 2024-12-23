from aiogram import Router
from ..admin.handlers import router as admin_start_router


admin_router = Router()
admin_router.include_router(admin_start_router)