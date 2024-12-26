from aiogram import Router
from .user.quiz_about_user.handlers import router as registration_router
from .user.my_team.handlers import router as my_team_router
from .user.test_task.handlers import router as test_task_router

user_router = Router()
user_router.include_router(registration_router)
user_router.include_router(my_team_router)
user_router.include_router(test_task_router)


