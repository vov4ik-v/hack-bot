from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from motor.core import AgnosticDatabase

from bot.sections.user.my_team.services import user_has_team, update_user_cv, update_team_github, unset_user_team, \
    get_team_by_name, set_user_team, create_team
from bot.sections.user.my_team.states import TeamCreationStates, TeamJoinStates, TeamGitHubStates, TeamCVStates
from bot.sections.user.quiz_about_user.services import is_user_registered
from bot.stages.utils.stages_service import get_current_stage
from bot.utils.keyboards.team_keyboard import get_team_keyboard, cancel_send_cv_keyboard, handle_find_team_keyboard, \
    cancel_send_github_keyboard
from bot.utils.middleware.Time import is_duplicate_request
from bot.utils.validators.my_team_validator import validate_text_only
from bot.stages.utils.bot_stage_filter import BotStageFilter
from bot.utils.keyboards.start_keyboard import get_start_keyboard, get_user_team_info
from bot.sections.user.my_team.services import send_team_info
from bot.sections.user.my_team.data import photo_path_team_image, text_find_team, chat_link

router = Router()

@router.message(F.text == "Моя Команда👥", BotStageFilter("before_registration"))
async def handle_team_before_registration(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return
    photo = FSInputFile(photo_path_team_image)
    await message.answer_photo(photo=photo, caption="Дочекайся початку реєстрації, щоб створити або долучитись до команди💻")

@router.message(F.text == "Моя Команда👥", BotStageFilter(["registration","test", "before_event","event"]))
async def handle_team_registration(message: types.Message, db: AgnosticDatabase):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    await send_team_info(message, db, user_id)

@router.message(F.text == "Знайти команду🔍")
async def handle_find_team(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(photo_path_team_image)
    reply_markup = handle_find_team_keyboard()
    await message.answer_photo(photo=photo, caption=text_find_team, reply_markup=reply_markup, parse_mode="HTML")

@router.message(F.text == "Головне меню🏠")
async def handle_back(message: types.Message, db):
    user_id = message.from_user.id
    message_text = message.text or ""
    test_approved, event_approved = await get_user_team_info(db, message.from_user.id)

    if is_duplicate_request(user_id, message_text):
        return

    is_registered = await is_user_registered(db, message.from_user.username)
    stage = await get_current_stage(db)
    main_kb = get_start_keyboard(stage, is_registered, test_approved, event_approved)
    await message.answer("Ви вернулись в головне меню.", reply_markup=main_kb)

@router.callback_query(F.data == "create_team")
async def cmd_create_team(callback_query: types.CallbackQuery, state: FSMContext, db: AgnosticDatabase):
    user_id = callback_query.from_user.id
    current_stage = await get_current_stage(db)
    if current_stage != "registration":
        await callback_query.message.answer("На жаль, <b>реєстрацію вже завершено!</b> Чекаємо тебе наступного року 🫂", parse_mode="HTML")
        return
    if await user_has_team(db, user_id):
        await callback_query.message.answer("Ти вже в команді. Спочатку вийди з неї, щоб створити нову.")
        return
    await callback_query.message.answer("Введи логін (одним повідомленням).")
    await state.set_state(TeamCreationStates.waiting_for_team_name)

@router.message(TeamCreationStates.waiting_for_team_name)
async def process_team_name(message: types.Message, state: FSMContext):
    if not await validate_text_only(message):
        return
    team_name = message.text.strip()
    if len(team_name) < 2 or len(team_name) > 15:
        await message.answer("Назва команди має містити від 2 до 15 символів. Спробуй ще раз.")
        return
    await state.update_data(team_name=team_name)
    await message.answer("Чудово! Тепер введи пароль для команди.")
    await state.set_state(TeamCreationStates.waiting_for_team_password)

@router.message(TeamCreationStates.waiting_for_team_password)
async def process_team_password(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    if not await validate_text_only(message):
        return
    password = message.text.strip()
    user_id = message.from_user.id
    data = await state.get_data()
    team_name = data.get("team_name")
    existing_team = await get_team_by_name(db, team_name)
    if existing_team:
        await message.answer(f"Команда з назвою <b>{team_name}</b> вже існує. Обери іншу назву або приєднайся до неї.",
                             parse_mode="HTML")
        await state.clear()
        return
    team_id = await create_team(db, team_name, password)
    await set_user_team(db, user_id, team_id)
    await state.clear()
    await message.answer(f"Команда {team_name} успішно створена.🎉")
    await send_team_info(message, db, user_id)

@router.callback_query(F.data == "join_team")
async def cmd_join_team(callback_query: types.CallbackQuery, state: FSMContext, db: AgnosticDatabase):
    user_id = callback_query.from_user.id
    current_stage = await get_current_stage(db)
    if current_stage != "registration":
        await callback_query.message.answer("На жаль, <b>реєстрацію вже завершено!</b> Чекаємо тебе наступного року 🫂", parse_mode="HTML")
        return
    if await user_has_team(db, user_id):
        await callback_query.message.answer("Ти вже в команді. Спочатку покинь її, щоб приєднатися до нової.")
        return
    await callback_query.message.answer("Введи логін команди, до якої хочеш приєднатися.")
    await state.set_state(TeamJoinStates.waiting_for_team_name)

@router.message(TeamJoinStates.waiting_for_team_name)
async def process_join_team_name(message: types.Message, state: FSMContext):
    if not await validate_text_only(message):
        return
    team_name = message.text.strip()
    await state.update_data(team_name=team_name)
    await message.answer("Тепер введи пароль команди:")
    await state.set_state(TeamJoinStates.waiting_for_team_password)

@router.message(TeamJoinStates.waiting_for_team_password)
async def process_join_team_password(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    if not await validate_text_only(message):
        return

    password = message.text.strip()
    user_id = message.from_user.id
    data = await state.get_data()
    team_name = data.get("team_name")
    team_doc = await get_team_by_name(db, team_name)
    if not team_doc:
        await message.answer(f"Команду з назвою <b>{team_name}</b> не знайдено.", parse_mode="HTML")
        await state.clear()
        return
    if team_doc.get("password") != password:
        await message.answer("Неправильний пароль. Спробуй ще раз або скасуй дію.❌")
        return

    team_id = team_doc["_id"]
    member_count = await db.get_collection("users").count_documents({"team_id": team_id})
    if member_count >= 5:
        await message.answer(
            f"Команда <b>{team_doc['name']}</b> вже має 5 учасників і не може прийняти більше.",
            parse_mode="HTML"
        )
        await state.clear()
        return
    await set_user_team(db, user_id, team_id)
    await state.clear()
    await message.answer(
        f"Вітаємо! Тепер ти в команді {team_doc['name']}.",
        reply_markup=get_team_keyboard(True)
    )
    await send_team_info(message, db, user_id)


@router.message(F.text == "Покинути команду🚪")
async def cmd_leave_team(message: types.Message, db: AgnosticDatabase):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    stage = await get_current_stage(db)
    username = message.from_user.username
    is_registered = await is_user_registered(db, username)
    test_approved, event_approved = await get_user_team_info(db, message.from_user.id)

    if stage != "registration":
        await message.answer("Покинути команду вже не можна.", reply_markup=get_team_keyboard(True))
        return
    if not await user_has_team(db, user_id):
        await message.answer("Ти ще не в жодній команді.")
        return
    await unset_user_team(db, user_id)
    await message.answer("Ти покинув(-ла) команду.", reply_markup=get_start_keyboard(stage, is_registered, test_approved, event_approved))

@router.message(F.text == "Надіслати GitHub-репозиторій📂")
async def cmd_send_github(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    # current_stage = await get_current_stage(db)
    # if current_stage != "registration":
    #     await message.answer("Час додавання GitHub-репозиторію вже сплинув.")
    #     return
    if not await user_has_team(db, user_id):
        await message.answer("Спочатку приєднайся до команди або створи свою.")
        return
    await message.answer(
        "Надішли мені посилання на GitHub-репозиторій проєкту (одним повідомленням). "
        "Якщо передумав(-ла), відправ 'Скасувати'.",
        reply_markup=cancel_send_github_keyboard()
    )
    await state.set_state(TeamGitHubStates.waiting_for_github_link)

@router.message(F.text == "Скасувати❌", TeamGitHubStates.waiting_for_github_link)
async def cancel_github_upload(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    await state.clear()
    await message.answer("Додавання GitHub-репозиторію скасовано.❌", reply_markup=get_team_keyboard(True))


@router.message(TeamGitHubStates.waiting_for_github_link)
async def process_github_link(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    if not await validate_text_only(message):
        return
    link = message.text.strip()
    user_id = message.from_user.id
    if not link.startswith("https://"):
        await message.answer("Посилання має починатися з https://. Спробуй ще раз.⚠️")
        return
    users_collection = db.get_collection("users")
    user_doc = await users_collection.find_one({"chat_id": user_id})
    team_id = user_doc.get("team_id")
    if not team_id:
        await message.answer("Упс! Ти не маєш команди.😶‍🌫️")
        await state.clear()
        return
    await update_team_github(db, team_id, link)
    await state.clear()
    await message.answer("GitHub-репозиторій успішно збережено!✅", reply_markup=get_team_keyboard(True))

@router.message(F.text == "Надіслати резюме📄")
async def cmd_send_cv(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    # current_stage = await get_current_stage(db)
    # if current_stage != "registration":
    #     await message.answer("Час додавання резюме вже сплинув.")
    #     return
    await message.answer(
        "Надішли мені свій PDF-файл із резюме (або будь-який інший формат, який підтримує TG). 📄Якщо передумав(-ла), відправ 'Скасувати'.", reply_markup=cancel_send_cv_keyboard()
    )
    await state.set_state(TeamCVStates.waiting_for_cv)

@router.message(F.text == "Скасувати❌", TeamCVStates.waiting_for_cv)
async def cancel_cv_upload(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    await state.clear()
    await message.answer("Завантаження CV скасовано.❌", reply_markup=get_team_keyboard(True))

@router.message(TeamCVStates.waiting_for_cv, F.document)
async def process_cv_document(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    document = message.document
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 МБ у байтах

    if document.file_size > MAX_FILE_SIZE:
        await state.clear()
        await message.answer(
            "Файл занадто великий. Максимальний розмір файлу має бути 50 МБ. Спробуй надіслати інший файл.",
            reply_markup=get_team_keyboard(True)
        )
        return

    user_id = message.from_user.id
    await update_user_cv(
        db,
        user_id=user_id,
        file_id=document.file_id,
        file_name=document.file_name or "resume",
        file_size=document.file_size,
    )
    await state.clear()
    await message.answer("Резюме успішно отримано і збережено!✅", reply_markup=get_team_keyboard(True))


@router.message(TeamCVStates.waiting_for_cv)
async def fallback_cv_upload(message: types.Message):
    await message.answer("Будь ласка, надішли файл із резюме або введи 'Скасувати', щоб скасувати.", reply_markup=cancel_send_cv_keyboard())

@router.message(TeamGitHubStates.waiting_for_github_link)
async def fallback_github_upload(message: types.Message):
    await message.answer(
        "Будь ласка, надішли правильне посилання на GitHub або введи 'Скасувати', щоб скасувати.",
        reply_markup=cancel_send_github_keyboard()
    )
