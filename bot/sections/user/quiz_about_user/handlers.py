from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    FSInputFile,
    ReplyKeyboardRemove,
)
from motor.core import AgnosticDatabase

from bot.sections.user.quiz_about_user.data import messages, photos
from bot.sections.user.quiz_about_user.services import is_user_registered
from bot.sections.user.quiz_about_user.services import process_registration_data
from bot.sections.user.quiz_about_user.states import RegistrationStates
from bot.stages.utils.stages_service import get_current_stage
from bot.utils.keyboards.start_keyboard import get_start_keyboard
from bot.utils.keyboards.user_registration_keyboard import consent_keyboard, contact_keyboard, course_keyboard, \
    university_keyboard
from bot.utils.validators.user_registration_validator import validate_age, validate_email, \
    validate_course, validate_text_input, validate_contact_input, validate_consent

router = Router()

@router.message(F.text == "📝 Реєстрація")
async def registration(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    username = message.from_user.username
    chat_id = message.chat.id

    current_stage = await get_current_stage(db)
    if current_stage not in ["before_registration", "registration"]:
        await message.answer(messages["registration_already_end"])
        return

    if await is_user_registered(db, username):
        await message.answer(messages["already_registered"])
        return

    await state.update_data(chat_id=chat_id)
    await message.answer(messages["registration_start"])
    await state.set_state(RegistrationStates.waiting_for_name)


@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer("Введи ім’я текстом 🤡")
        return
    await state.update_data(name=message.text)
    await message.answer(messages["name_correct"])
    await message.answer(messages["age_prompt"])
    await state.set_state(RegistrationStates.waiting_for_age)


@router.message(RegistrationStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not validate_age(message):
        await message.answer(messages["age_incorrect"])
        return
    await state.update_data(age=message.text)
    await message.answer(messages["university_prompt"], reply_markup=university_keyboard)
    await state.set_state(RegistrationStates.waiting_for_university)

@router.message(RegistrationStates.waiting_for_university)
async def process_university(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer(messages["university_incorrect"], reply_markup=university_keyboard)
        return
    await state.update_data(university=message.text)
    await message.answer(messages["course_prompt"], reply_markup=course_keyboard)
    await state.set_state(RegistrationStates.waiting_for_course)

@router.message(RegistrationStates.waiting_for_course)
async def process_course(message: types.Message, state: FSMContext):
    if not validate_course(message):
        await message.answer(messages["course_incorrect"], reply_markup=course_keyboard)
        return
    await state.update_data(course=message.text)
    await message.answer(messages["technologies_prompt"])
    await state.set_state(RegistrationStates.waiting_for_technologies)


@router.message(RegistrationStates.waiting_for_technologies)
async def process_technologies(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer("Відповідь треба записувати текстом")
        return
    await state.update_data(technologies=message.text)
    await message.answer(messages["technologies_correct"])
    await message.answer(messages["source_prompt"])
    await state.set_state(RegistrationStates.waiting_for_source)


@router.message(RegistrationStates.waiting_for_source)
async def process_source(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer("Відповідь треба записувати текстом")
        return
    await state.update_data(source=message.text)
    await message.answer(messages["source_correct"])
    await message.answer(messages["it_experience_prompt"])
    await state.set_state(RegistrationStates.waiting_for_it_experience)


@router.message(RegistrationStates.waiting_for_it_experience)
async def process_it_experience(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer("Відповідь треба записувати текстом")
        return
    await state.update_data(it_experience=message.text)
    await message.answer(messages["it_experience_correct"])
    await message.answer(messages["contact_prompt"], reply_markup=contact_keyboard)
    await state.set_state(RegistrationStates.waiting_for_contact)


@router.message(F.contact, RegistrationStates.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    if not validate_contact_input(message):
        await message.answer(messages["contact_incorrect"])
        return
    contact_info = {
        "phone_number": message.contact.phone_number,
        "username": message.from_user.username
    }
    await state.update_data(contact=contact_info)
    await message.answer(
        messages["contact_correct"],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(messages["email_prompt"])
    await state.set_state(RegistrationStates.waiting_for_email)


@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    if not validate_email(message):
        await message.answer(messages["email_incorrect"])
        return
    await state.update_data(email=message.text)
    await message.answer(messages["email_correct"])
    await message.answer(messages["consent_prompt"], reply_markup=consent_keyboard)
    await state.set_state(RegistrationStates.waiting_for_consent)


@router.callback_query(F.data == "consent_yes")
async def process_consent(callback: types.CallbackQuery, state: FSMContext, db: AgnosticDatabase):
    if not validate_consent(callback.data):
        await callback.answer("Будь ласка, натисни 'Погоджуюсь' для підтвердження.")
        return

    await callback.answer(messages["consent_received"])

    try:
        photo = FSInputFile(photos["success_register_photo"])

        state_data = await state.get_data()
        user_data = await process_registration_data(db, state_data)

        await state.clear()

        username = callback.from_user.username
        is_registered = await is_user_registered(db, username)
        stage = await get_current_stage(db)

        updated_keyboard = get_start_keyboard(stage, is_registered)

        await callback.message.answer_photo(photo=photo, caption=messages["registration_complete"], reply_markup=updated_keyboard)

    except Exception as e:
        print(f"Помилка при збереженні даних: {e}")
        await callback.message.answer(messages["registration_error"])