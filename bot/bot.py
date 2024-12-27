from aiogram import Bot, Dispatcher
from config_reader import BOT_TOKEN
from .sections import user_router
from .sections.admin import admin_router
from .sections.start import start_router
from .stages import stages_router
from .utils.validators.AlwaysKeyboardMiddleware import AlwaysKeyboardMiddleware



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.message.middleware(AlwaysKeyboardMiddleware())
# dp.message.middleware(ThrottlingMiddleware())

dp.include_routers(
    start_router,
    admin_router,
    user_router,
    stages_router
)
