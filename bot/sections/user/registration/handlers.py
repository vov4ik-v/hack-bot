from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from motor.core import AgnosticDatabase
from bot.sections.user.registration.services import is_user_registered

from bot.sections.user.registration.services import process_registration_data
from bot.utils.keyboards.start_keyboard import get_start_keyboard
from bot.utils.keyboards.user_registration_keyboard import consent_keyboard, contact_keyboard, course_keyboard, \
    university_keyboard
from bot.utils.validators.user_registration_validator import validate_age, validate_email, validate_university, \
    validate_course

router = Router()
photo_path = "asset/hack_register_photo.jpg"

# Визначаємо всі стани
class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_university = State()
    waiting_for_course = State()
    waiting_for_technologies = State()
    waiting_for_source = State()
    waiting_for_it_experience = State()
    waiting_for_contact = State()
    waiting_for_email = State()
    waiting_for_consent = State()



@router.message(F.text == "📝 Реєстрація")
async def registration(message: types.Message, state: FSMContext, db: AgnosticDatabase):
    username = message.from_user.username
    chat_id = message.chat.id

    if await is_user_registered(db, username):
        await message.answer("🎉 Ти чемпіон і вже зареєстрований на BEST::HACKath0n! 🥇 Якщо хочеш оновити інформацію, звернись до організаторів 🤗")
        return

    await state.update_data(chat_id=chat_id)
    await message.answer("Як мені до тебе звертатися?")
    await state.set_state(RegistrationStates.waiting_for_name)


@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Гарно звучить 🥰")
    await message.answer("Скільки тобі років?")
    await state.set_state(RegistrationStates.waiting_for_age)


@router.message(RegistrationStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not validate_age(message.text):
        await message.answer("Будь ласка, введи коректний вік (число від 10 до 100).")
        return
    await state.update_data(age=message.text)
    await message.answer("Де вчишся? Вибери університет або введи.", reply_markup=university_keyboard)
    await state.set_state(RegistrationStates.waiting_for_university)

@router.message(RegistrationStates.waiting_for_university)
async def process_university(message: types.Message, state: FSMContext):
    if not validate_university(message.text):
        await message.answer("Будь ласка, вибери університет зі списку: НУЛП або ЛНУ.")
        return
    await state.update_data(university=message.text)
    await message.answer("Який ти курс?", reply_markup=course_keyboard)
    await state.set_state(RegistrationStates.waiting_for_course)

@router.message(RegistrationStates.waiting_for_course)
async def process_course(message: types.Message, state: FSMContext):
    if not validate_course(message.text):
        await message.answer("Будь ласка, вибери курс від 1 до 5.")
        return
    await state.update_data(course=message.text)
    await message.answer("Які технології збираєшся використовувати на проєкті?(Перерархуй через кому)")
    await state.set_state(RegistrationStates.waiting_for_technologies)


@router.message(RegistrationStates.waiting_for_technologies)
async def process_technologies(message: types.Message, state: FSMContext):
    await state.update_data(technologies=message.text)
    await message.answer("Те що треба!")
    await message.answer("Звідки дізнався про Hackathon?")
    await state.set_state(RegistrationStates.waiting_for_source)


@router.message(RegistrationStates.waiting_for_source)
async def process_source(message: types.Message, state: FSMContext):
    await state.update_data(source=message.text)
    await message.answer("Дякую за відповідь, для мене це дуже корисно)")
    await message.answer("Вже працюєш в айті сфері?")
    await state.set_state(RegistrationStates.waiting_for_it_experience)


@router.message(RegistrationStates.waiting_for_it_experience)
async def process_it_experience(message: types.Message, state: FSMContext):
    await state.update_data(it_experience=message.text)
    await message.answer("Дякую за інформацію)")
    await message.answer("Обміняємося контактами? Натисни 'Поділитись контактом' нижче 👇", reply_markup=contact_keyboard)
    await state.set_state(RegistrationStates.waiting_for_contact)


@router.message(F.contact, RegistrationStates.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact_info = {
        "phone_number": message.contact.phone_number,
        "username": message.from_user.username
    }
    await state.update_data(contact=contact_info)
    await message.answer(
        "А я залишаю тобі контакт головного організатора: @sonyoe 🥰",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer("Наостанок, вкажи адресу своєї поштової скриньки.")
    await state.set_state(RegistrationStates.waiting_for_email)


@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    if not validate_email(message.text):
        await message.answer("Будь ласка, введи коректний email у форматі example@example.com.")
        return
    await state.update_data(email=message.text)
    await message.answer("Дякую 🥰")
    await message.answer("Залишилося тільки дати згоду на обробку даних. Натисни 'Погоджуюсь' для підтвердження.", reply_markup=consent_keyboard)
    await state.set_state(RegistrationStates.waiting_for_consent)


@router.callback_query(F.data == "consent_yes")
async def process_consent(callback: types.CallbackQuery, state: FSMContext, db: AgnosticDatabase):
    await callback.answer("Згоду отримано!")

    try:
        success_register_photo_path = "asset/hack_register_photo.jpg"
        photo = FSInputFile(success_register_photo_path)

        state_data = await state.get_data()
        user_data = await process_registration_data(db, state_data)
        print("user_data", user_data)

        await state.clear()

        username = callback.from_user.username
        is_registered = await is_user_registered(db, username)
        updated_keyboard = get_start_keyboard(is_registered)



        await callback.message.answer_photo(photo= photo,caption=
            """Вітаю із завершенням реєстрації! 🎉
Тепер ти зможеш:
      - Знайти команду
      - Сформувати команду
      - Пройти тестове завдання
      - Зайти в чат, де будуть всі учасники
      - Отримати всю інформацію про змагання
      Та багато іншого!""",
            reply_markup=updated_keyboard
        )

    except Exception as e:
        print(f"Помилка при збереженні даних: {e}")
        await callback.message.answer(
            "Щось пішло не так під час реєстрації. Будь ласка, спробуй ще раз або звернися до адміністратора."
        )

