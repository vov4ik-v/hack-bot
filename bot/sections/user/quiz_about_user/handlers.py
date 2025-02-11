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
from bot.utils.keyboards.start_keyboard import get_start_keyboard, get_user_team_info
from bot.utils.keyboards.user_registration_keyboard import consent_keyboard, contact_keyboard, course_keyboard, \
    university_keyboard, get_source_keyboard, get_it_experience_keyboard
from bot.utils.middleware.Time import is_duplicate_request
from bot.utils.validators.user_registration_validator import validate_email, \
    validate_text_input, validate_contact_input, validate_consent, validate_course, validate_it_experience, \
    validate_length, validate_name, validate_university, validate_source, validate_it_experience_length, \
    validate_email_length, validate_age_format, validate_age_range

router = Router()

@router.message(F.text == "📝 Реєстрація")
async def registration(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    username = message.from_user.username
    chat_id = message.chat.id

    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    current_stage = await get_current_stage(db)
    if current_stage not in ["before_registration", "registration"]:
        await message.answer(messages["registration_already_end"], parse_mode="HTML")
        return

    if await is_user_registered(db, username):
        await message.answer(messages["already_registered"], parse_mode="HTML")
        return

    await state.update_data(chat_id=chat_id)
    await message.answer(messages["registration_start"], parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.waiting_for_name)


@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer("Введи ім’я текстом 😜", reply_markup=ReplyKeyboardRemove())
        return
    if not validate_name(message):
        await message.answer("Кількість символів перевищено. Максимальна кількість символів: 20.",
                             reply_markup=ReplyKeyboardRemove())
        return

    await state.update_data(name=message.text)
    await message.answer(messages["name_correct"], parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

    await message.answer(messages["age_prompt"], parse_mode="HTML")
    await state.set_state(RegistrationStates.waiting_for_age)


@router.message(RegistrationStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not validate_age_format(message):
        await message.answer("Будь ласка, введи число 📊", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        return

    if not validate_age_range(message):
        await message.answer(messages["age_incorrect"], parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        return

    await state.update_data(age=int(message.text))
    await message.answer(messages["university_prompt"], parse_mode="HTML", reply_markup=university_keyboard)
    await state.set_state(RegistrationStates.waiting_for_university)

@router.message(RegistrationStates.waiting_for_university)
async def process_university(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    if not validate_text_input(message):
        await message.answer(messages["university_incorrect"], parse_mode="HTML", reply_markup=university_keyboard)
        return

    if not validate_university(message):
        await message.answer("Кількість символів перевищено. Максимальна кількість символів: 25.")
        return

    university = message.text
    if university in ["Ще в школі", "Вже закінчив (-ла)"]:
        await message.answer("На жаль, ці змагання тільки для студентів. Дякуємо за інтерес 💚",
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    await state.update_data(university=university)
    await message.answer(messages["course_prompt"], parse_mode="HTML", reply_markup=course_keyboard)
    await state.set_state(RegistrationStates.waiting_for_course)

@router.message(RegistrationStates.waiting_for_course)
async def process_course(message: types.Message, state: FSMContext):
    if not validate_course(message):
        await message.answer(messages["course_incorrect"], parse_mode="HTML", reply_markup=course_keyboard)
        return

    await state.update_data(course=message.text)
    await message.answer(messages["technologies_prompt"], parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.waiting_for_technologies)


@router.message(RegistrationStates.waiting_for_technologies)
async def process_technologies(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer("Відповідь треба записувати текстом 😜")
        return
    await state.update_data(technologies=message.text)
    await message.answer(messages["technologies_correct"], parse_mode="HTML")
    await message.answer(messages["source_prompt"], parse_mode="HTML", reply_markup=get_source_keyboard())
    await state.set_state(RegistrationStates.waiting_for_source)


@router.message(RegistrationStates.waiting_for_source)
async def process_source(message: types.Message, state: FSMContext):
    if not validate_text_input(message):
        await message.answer("Відповідь треба записувати текстом 😜")
        return

    if not validate_source(message):
        await message.answer("Кількість символів перевищено. Максимальна кількість символів: 50.")
        return

    await state.update_data(source=message.text)
    await message.answer(messages["source_correct"], parse_mode="HTML")
    await message.answer(messages["it_experience_prompt"], parse_mode="HTML", reply_markup=get_it_experience_keyboard())
    await state.set_state(RegistrationStates.waiting_for_it_experience)


@router.message(RegistrationStates.waiting_for_it_experience)
async def process_it_experience(message: types.Message, state: FSMContext):
    if not validate_it_experience(message):
        await message.answer("Обери один із варіантів – так буде простіше 🎯")
        return

    if not validate_it_experience_length(message):
        await message.answer("Кількість символів перевищено. Максимальна кількість символів: 15.")
        return
    await state.update_data(it_experience=message.text)
    await message.answer(messages["it_experience_correct"], parse_mode="HTML")
    await message.answer(messages["contact_prompt"], parse_mode="HTML", reply_markup=contact_keyboard)
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
        messages["contact_correct"], parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(messages["email_prompt"], parse_mode="HTML")
    await state.set_state(RegistrationStates.waiting_for_email)


@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    if not validate_email(message):
        await message.answer(messages["email_incorrect"], parse_mode="HTML")
        return

    if not validate_email_length(message):
        await message.answer("Кількість символів перевищено. Максимальна кількість символів: 35.")
        return
    await state.update_data(email=message.text)
    await message.answer(messages["email_correct"], parse_mode="HTML")
    await message.answer(messages["consent_prompt"], parse_mode="HTML", reply_markup=consent_keyboard)
    await state.set_state(RegistrationStates.waiting_for_consent)


@router.message(RegistrationStates.waiting_for_consent)
async def process_consent_input(message: types.Message, state: FSMContext):
    await message.answer(
        "Будь ласка, натисни 'Погоджуюсь' для підтвердження.",
        reply_markup=consent_keyboard
    )

@router.callback_query(F.data == "consent_yes")
async def process_consent(
    callback: types.CallbackQuery,
    state: FSMContext,
    db: AgnosticDatabase
):
    test_approved, event_approved = await get_user_team_info(db, callback.from_user.id)

    if not validate_consent(callback.data):
        await callback.answer("Будь ласка, натисни 'Погоджуюсь' для підтвердження.")
        return

    await callback.answer(messages["consent_received"], parse_mode="HTML")

    try:
        photo = FSInputFile(photos["success_register_photo"])
        state_data = await state.get_data()
        user_data = await process_registration_data(db, state_data)
        await state.clear()

        username = callback.from_user.username
        is_registered = await is_user_registered(db, username)
        stage = await get_current_stage(db)

        updated_keyboard = get_start_keyboard(stage, is_registered, test_approved, event_approved)

        await callback.message.answer_photo(
            photo=photo,
            caption=messages["registration_complete"],
            parse_mode="HTML",
            reply_markup=updated_keyboard
        )

    except Exception as e:
        print(f"Помилка при збереженні даних: {e}")
        await callback.message.answer(messages["registration_error"])
