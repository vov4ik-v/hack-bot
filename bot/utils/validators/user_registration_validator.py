import re
from aiogram.types import Message, Contact

def validate_text_input(message: Message, max_length: int = 4000) -> bool:
    if not message.text or len(message.text) > max_length:
        return False
    return True

def validate_length(message: Message, max_length: int, field_name: str) -> bool:
    if not message.text:
        return False
    if len(message.text) > max_length:
        return False
    return True

def validate_regex(message: Message, pattern: str) -> bool:
    if not message.text or not re.match(pattern, message.text):
        return False
    return True

def validate_contact_input(message: Message) -> bool:
    return isinstance(message.contact, Contact)

def validate_age(message: Message) -> bool:
    if not message.text or not message.text.isdigit():
        return False
    age = int(message.text)
    return 16 <= age <= 100

def validate_it_experience(message: Message) -> bool:
    valid_experience = {"Так", "Ні", "Планую"}
    return message.text in valid_experience

def validate_course(message: Message) -> bool:
    valid_courses = {
        "перший": 1,
        "другий": 2,
        "третій": 3,
        "четвертий": 4,
        "на магістратурі": "магістратура",
        "нічого з переліченого": "інше"
    }
    user_input = message.text.strip().lower()
    if user_input.isdigit():
        return int(user_input) in valid_courses.values()
    else:
        return user_input in valid_courses

def validate_email_length(message: Message) -> bool:
    return validate_length(message, 35, "Електронна пошта")

def validate_email(message: Message) -> bool:
    pattern = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
    return validate_regex(message, pattern)

def validate_source(message: Message) -> bool:
    return validate_length(message, 50, "Джерело інформації")

def validate_technologies(message: Message) -> bool:
    return validate_text_input(message)

def validate_university(message: Message) -> bool:
    return validate_length(message, 15, "Університет")

def validate_name(message: Message) -> bool:
    return validate_length(message, 20, "Ім'я")

def validate_it_experience_length(message: Message) -> bool:
    return validate_length(message, 15, "Досвід у ІТ")

def validate_consent(callback_data: str) -> bool:
    return callback_data == "consent_yes"
