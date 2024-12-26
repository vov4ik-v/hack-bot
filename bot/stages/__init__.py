from aiogram import Router


from .before_registration.handlers import router as before_registration_router
from .registration.handlers import router as registration_router
from .before_event.handlers import router as before_event_router
from .event.handlers import router as event_router
from .after_event.handlers import router as after_event_router


stages_router = Router()
stages_router.include_router(before_registration_router)
stages_router.include_router(registration_router)
stages_router.include_router(before_event_router)
stages_router.include_router(event_router)
stages_router.include_router(after_event_router)



