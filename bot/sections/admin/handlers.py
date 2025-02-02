import os
import zipfile

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.types import Message, CallbackQuery
from bson import ObjectId
from motor.core import AgnosticDatabase

from bot.sections.admin.data import *
from bot.sections.admin.services import *
from bot.sections.admin.states import StageSelectionStates, BroadcastStates, TeamMessageState
from bot.sections.user.quiz_about_user.services import is_user_registered
from bot.utils.keyboards.admin_keyboard import get_main_admin_keyboard, get_stage_selection_keyboard, \
    get_broadcast_inline_keyboard, get_team_actions_inline_keyboard
from bot.utils.keyboards.start_keyboard import get_start_keyboard
from config_reader import ADMIN_PASSWORD

router = Router()


@router.message(F.text == str(ADMIN_PASSWORD))
async def open_admin_panel(message: types.Message):
    await message.answer(ADMIN_WELCOME, reply_markup=get_main_admin_keyboard())


@router.message(F.text == "Вийти з адмінки")
async def handle_admin_exit(message: Message, db: AgnosticDatabase):
    is_registered = await is_user_registered(db, message.from_user.username)
    stage = await get_current_stage(db)
    await message.answer(ADMIN_EXIT, reply_markup=get_start_keyboard(stage, is_registered))


@router.message(F.text == "Переключити секцію")
async def handle_toggle_section(message: Message, state: FSMContext):
    await message.answer(STAGE_SELECTION_PROMPT, reply_markup=get_stage_selection_keyboard())
    await state.set_state(StageSelectionStates.waiting_for_stage)


@router.message(StageSelectionStates.waiting_for_stage)
async def process_stage_selection(message: Message, state: FSMContext, db: AgnosticDatabase):
    chosen_stage = message.text.strip()
    stage_mapping = {
        "Початок реєстрації": "before_registration",
        "Реєстрація": "registration",
        "Підготовка до івенту": "before_event",
        "Івент": "event",
        "Після івенту": "after_event"
    }
    valid_stages = stage_mapping.keys()

    if chosen_stage == "Скасувати зміну стадії":
        await message.answer(STAGE_SELECTION_CANCEL, reply_markup=get_main_admin_keyboard())
        await state.clear()
        return

    if chosen_stage not in valid_stages:
        await message.answer(STAGE_SELECTION_INVALID, reply_markup=get_stage_selection_keyboard())
        return

    new_stage = stage_mapping[chosen_stage]
    await update_stage(db, new_stage)

    all_users = await get_all_users(db)
    teams_passed_test = await get_teams_by_test_status(db, True)
    teams_not_passed_test = await get_teams_by_test_status(db, False)
    team_ids_passed = [team["_id"] for team in teams_passed_test]
    team_ids_not_passed = [team["_id"] for team in teams_not_passed_test]

    if new_stage in ["before_registration", "registration"]:
        message_text = "Ураа! Реєстрація розпочата!" if new_stage == "registration" else "Початок реєстрації!"
        for user in all_users:
            chat_id = user.get("chat_id")
            print(f"Sending message to {chat_id}", user.get("username"))
            await is_user_registered(db, user.get("username"))
            if chat_id:
                try:
                    await message.bot.send_message(chat_id, message_text,
                                                   reply_markup=get_start_keyboard(new_stage, True))
                except Exception as e:
                    print(f"Помилка надсилання повідомлення користувачу {chat_id}: {e}")

    elif new_stage == "before_event":
        for team_id in team_ids_passed:
            recipients = await get_users_by_team_ids(db, [team_id])
            for recipient in recipients:
                chat_id = recipient.get("chat_id")
                if chat_id:
                    try:
                        await message.bot.send_message(chat_id, """
                        🚀 Привіт, майбутні чемпіони! Ви успішно виконали тестове завдання – це вже успіх! 🏆
Ваша команда - потенційний переможець BEST::HACKath0n 2025! Тепер для вас відкриваються ексклюзивні деталі проєкту. 🔥""",
                                                       reply_markup=get_start_keyboard(new_stage, True))
                    except Exception as e:
                        print(f"Помилка надсилання повідомлення користувачу {chat_id}: {e}")

        for team_id in team_ids_not_passed:
            recipients = await get_users_by_team_ids(db, [team_id])
            for recipient in recipients:
                chat_id = recipient.get("chat_id")
                if chat_id:
                    try:
                        await message.bot.send_message(chat_id, "Не плачте! Ви не пройшли тестове завдання.",
                                                       reply_markup=get_start_keyboard("registration", True))
                    except Exception as e:
                        print(f"Помилка надсилання повідомлення користувачу {chat_id}: {e}")

    elif new_stage in ["event", "after_event"]:
        message_text = "Івент розпочато!" if new_stage == "event" else "Івент завершено!"
        for team_id in team_ids_passed:
            recipients = await get_users_by_team_ids(db, [team_id])
            for recipient in recipients:
                chat_id = recipient.get("chat_id")
                if chat_id:
                    try:
                        await message.bot.send_message(chat_id, message_text,
                                                       reply_markup=get_start_keyboard(new_stage, True))
                    except Exception as e:
                        print(f"Помилка надсилання повідомлення користувачу {chat_id}: {e}")

    await message.answer(STAGE_SWITCHED.format(chosen_stage), reply_markup=get_main_admin_keyboard())
    await state.clear()


@router.message(F.text == "Розсилка")
async def handle_broadcast_menu(message: Message):
    await message.answer(BROADCAST_PROMPT, reply_markup=get_broadcast_inline_keyboard())


@router.callback_query(F.data.startswith("broadcast:"))
async def handle_broadcast_category_callback(query: CallbackQuery, state: FSMContext, db: AgnosticDatabase):
    category = query.data.split(":")[1]
    if category == "cancel":
        await query.message.edit_text(BROADCAST_CANCEL)
        await state.clear()
        return

    await state.update_data({"target": category})
    await state.set_state(BroadcastStates.waiting_for_message)
    await query.message.edit_text("Введіть текст повідомлення для розсилки:")


@router.message(BroadcastStates.waiting_for_message)
async def handle_broadcast_message(message: Message, state: FSMContext, db: AgnosticDatabase):
    data = await state.get_data()
    target = data.get("target")

    recipients = []
    if target == "all":
        recipients = await get_all_users(db)
    elif target == "in_teams":
        recipients = await db.get_collection("users").find({"team_id": {"$exists": True}}).to_list(length=None)
    elif target == "not_in_teams":
        recipients = await db.get_collection("users").find({"team_id": {"$exists": False}}).to_list(length=None)
    elif target == "teams_less_than_3":
        teams = await list_teams(db)
        team_ids = [team["_id"] for team in teams if
                    (await db.get_collection("users").count_documents({"team_id": team["_id"]}) < 3)]
        recipients = await get_users_by_team_ids(db, team_ids)
    elif target == "in_teams_passed_test":
        teams = await get_teams_by_test_status(db, True)
        team_ids = [team["_id"] for team in teams]
        recipients = await get_users_by_team_ids(db, team_ids)
    elif target == "in_teams_not_passed_test":
        teams = await get_teams_by_test_status(db, False)
        team_ids = [team["_id"] for team in teams]
        recipients = await get_users_by_team_ids(db, team_ids)

    if message.text:
        content_type = "text"
        content = message.text
    elif message.photo:
        content_type = "photo"
        content = message.photo[-1].file_id
        caption = message.caption or ""
    elif message.document:
        content_type = "document"
        content = message.document.file_id
        caption = message.caption or ""
    else:
        await message.answer("Непідтримуваний тип контенту. Будь ласка, надішліть текст, фото або документ.")
        return

    for recipient in recipients:
        chat_id = recipient.get("chat_id")
        if not chat_id:
            continue

        try:
            if content_type == "text":
                await message.bot.send_message(chat_id=chat_id, text=content)
            elif content_type == "photo":
                await message.bot.send_photo(chat_id=chat_id, photo=content, caption=caption)
            elif content_type == "document":
                await message.bot.send_document(chat_id=chat_id, document=content, caption=caption)
        except Exception as e:
            print(f"Помилка надсилання {content_type} користувачу {chat_id}: {e}")

    await message.answer(BROADCAST_COMPLETE.format(target), reply_markup=get_main_admin_keyboard())
    await state.clear()


@router.message(F.text == "Робота з командами")
async def handle_list_teams(message: Message, db: AgnosticDatabase):
    teams = await list_teams(db)
    if not teams:
        await message.answer(NO_TEAMS_AVAILABLE, reply_markup=get_main_admin_keyboard())
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=team.get('name', f"Команда {team['_id']}"),
                              callback_data=f"team:select:{team['_id']}")]
        for team in teams
    ])

    await message.answer(TEAM_SELECTION_PROMPT, reply_markup=kb)


@router.callback_query(F.data.startswith("team:select:"))
async def handle_select_team_callback(query: CallbackQuery, db: AgnosticDatabase):
    _, _, team_id = query.data.split(":")
    print("Selected team:", team_id)

    try:
        team_object_id = ObjectId(team_id)
    except Exception as e:
        print(f"Invalid ObjectId format: {team_id}")
        await query.answer(INVALID_TEAM_ID, show_alert=True)
        return

    team = await db.get_collection("teams").find_one({"_id": team_object_id})
    print("Team info:", team)
    if not team:
        await query.answer(TEAM_NOT_FOUND, show_alert=True)
        return

    team_name = team.get('name', f"team_{team_id}")
    await query.message.edit_text(TEAM_SELECTED.format(team_name),
                                  reply_markup=get_team_actions_inline_keyboard(str(team_id)))


@router.callback_query(F.data == "teams:return_list")
async def handle_return_to_team_list(query: CallbackQuery, db: AgnosticDatabase):
    teams = await list_teams(db)
    if not teams:
        await query.message.edit_text(NO_TEAMS_AVAILABLE, reply_markup=None)
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=team.get('name', f"Команда {team['_id']}"),
                              callback_data=f"team:select:{team['_id']}")]
        for team in teams
    ])

    await query.message.edit_text(TEAM_SELECTION_PROMPT, reply_markup=kb)


@router.callback_query(F.data.startswith("team:"))
async def handle_team_actions(query: CallbackQuery, db: AgnosticDatabase,state: FSMContext):
    parts = query.data.split(":")
    if len(parts) < 3:
        await query.answer(INVALID_DATA_FORMAT, show_alert=True)
        return

    action = parts[1]
    team_id = parts[2]

    try:
        team_object_id = ObjectId(team_id)
    except Exception as e:
        print(f"Invalid ObjectId format: {team_id}")
        await query.answer(INVALID_TEAM_ID, show_alert=True)
        return

    if action == "members":
        members_info = await get_team_members_info(db, team_object_id)
        text = members_info or "Учасників не знайдено."
        await query.message.answer(text)
        await query.answer()

    elif action == "repo":
        repo_link = await get_team_repo_link(db, team_object_id)
        text = repo_link or "Посилання на репозиторій не вказано."
        await query.message.answer(text)
        await query.answer()

    elif action == "tech":
        team_members = await db.get_collection("users").find({"team_id": team_object_id}).to_list(length=None)
        tech_info = [f"{member.get('name', 'Невідомо')}: {member.get('technologies', 'Технології не вказано')}" for
                     member in team_members]
        text = "\n".join(tech_info) if tech_info else "Технології не вказано."
        await query.message.answer(text)
        await query.answer()

    elif action == "cv":
        team_members = await db.get_collection("users").find({"team_id": team_object_id}).to_list(length=None)
        if not team_members:
            await query.answer("Учасників не знайдено.", show_alert=True)
            return

        zip_filename = f"team_{team_id}_cvs.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for member in team_members:
                resume = member.get("resume")
                if resume:
                    file_id = resume["file_id"]
                    file_name = resume["file_name"]
                    file = await query.bot.get_file(file_id)
                    file_path = file.file_path
                    await query.bot.download_file(file_path, file_name)
                    zipf.write(file_name, file_name)
                    os.remove(file_name)

        await query.message.answer_document(FSInputFile(zip_filename))
        os.remove(zip_filename)  # Clean up the zip file
        await query.answer("CVs завантажено.")


    elif action == "approve_test":

        await approve_test_submission(db, team_object_id)

        await query.message.answer("Тестове завдання апрувнуто.")

        await query.answer()

        # Notify team members

        team_members = await db.get_collection("users").find({"team_id": team_object_id}).to_list(length=None)

        for member in team_members:

            chat_id = member.get("chat_id")

            if chat_id:

                try:

                    await query.bot.send_message(chat_id, "Вам апрувнули тестове завдання!")

                except Exception as e:

                    print(f"Помилка надсилання повідомлення користувачу {chat_id}: {e}")


    elif action == "approve_event":

        await approve_event_participation(db, team_object_id)

        await query.message.answer("Участь в івенті апрувнуто.")

        await query.answer()

        # Notify team members

        team_members = await db.get_collection("users").find({"team_id": team_object_id}).to_list(length=None)

        for member in team_members:

            chat_id = member.get("chat_id")

            if chat_id:

                try:

                    await query.bot.send_message(chat_id, "Вам апрувнули участь на івенті!")

                except Exception as e:

                    print(f"Помилка надсилання повідомлення користувачу {chat_id}: {e}")


    elif action == "delete":
        await delete_team(db, team_object_id)
        await query.message.answer("Команду видалено.")
        await query.answer()

        teams = await list_teams(db)
        if not teams:
            await query.message.answer(NO_TEAMS_AVAILABLE)
            return

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=team.get('name', f"Команда {team['_id']}"),
                                  callback_data=f"team:select:{str(team['_id'])}")]
            for team in teams
        ])
        await query.message.answer(TEAM_SELECTION_PROMPT, reply_markup=kb)

    if action == "message":
        # Зберігаємо team_id у FSM, щоб знати, кому надсилати
        await state.update_data({"team_id": team_id})
        # Переводимо користувача в стан написання повідомлення
        await state.set_state(TeamMessageState.waiting_for_message)
        # Пропонуємо адмінам ввести текст
        await query.message.answer("Введіть текст повідомлення, яке хочете надіслати цій команді:")
        await query.answer()
        return

    else:
        await query.answer(UNKNOWN_ACTION, show_alert=True)

@router.message(TeamMessageState.waiting_for_message)
async def handle_team_message(message: Message, state: FSMContext, db: AgnosticDatabase):
    data = await state.get_data()
    team_id = data.get("team_id")

    if not team_id:
        await message.answer("Не вдалося визначити команду. Спробуйте ще раз.")
        await state.clear()
        return

    content_type = None
    content = None
    caption = None

    if message.text:
        content_type = "text"
        content = message.text
    elif message.photo:
        content_type = "photo"
        content = message.photo[-1].file_id
        caption = message.caption or ""
    elif message.document:
        content_type = "document"
        content = message.document.file_id
        caption = message.caption or ""
    else:
        await message.answer("Непідтримуваний тип контенту. Будь ласка, надішліть текст, фото або документ.")
        return

    try:
        team_object_id = ObjectId(team_id)
    except:
        await message.answer("Невірний ID команди.")
        await state.clear()
        return

    team_members = await db.get_collection("users").find({"team_id": team_object_id}).to_list(length=None)

    for member in team_members:
        chat_id = member.get("chat_id")
        if not chat_id:
            continue

        try:
            if content_type == "text":
                await message.bot.send_message(chat_id=chat_id, text=content)
            elif content_type == "photo":
                await message.bot.send_photo(chat_id=chat_id, photo=content, caption=caption)
            elif content_type == "document":
                await message.bot.send_document(chat_id=chat_id, document=content, caption=caption)
        except Exception as e:
            print(f"Помилка надсилання {content_type} користувачу {chat_id}: {e}")

    await message.answer("Повідомлення надіслано всім учасникам команди.")
    await state.clear()

