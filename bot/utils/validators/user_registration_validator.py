import re
from aiogram.types import Message, Contact

def validate_text_input(message: Message, max_length: int = 4000) -> bool:
    if not message.text or len(message.text) > max_length:
        return False
    return True

def validate_regex(message: Message, pattern: str) -> bool:
    if not message.text or not re.match(pattern, message.text):
        return False
    return True

def validate_contact_input(message: Message) -> bool:
    if not isinstance(message.contact, Contact):
        return False
    return True

def validate_age(message: Message) -> bool:
    if not message.text or not message.text.isdigit():
        return False
    age = int(message.text)
    return 14 <= age <= 100


# def validate_university(message: Message) -> bool:
#     """
#     Validates if the university name is one of the accepted options.
#     """
#     valid_universities = {"НУЛП", "ЛНУ", "УКУ", "КПІ", "КНУ", "Ще в школі", "Вже закінчив(-ла)"}
#     return message.text in valid_universities

# def validate_course(message: Message) -> bool:
#     valid_courses = {"Перший", "Другий", "Третій", "Четвертий", "На магістартурі", "Нічого з переліченого"}
#     return message.text in valid_courses

def validate_email(message: Message) -> bool:
    pattern = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
    return validate_regex(message, pattern)

def validate_it_experience(message: Message) -> bool:
    valid_responses = {"Так", "Ні", "Планую"}
    return message.text in valid_responses

def validate_source(message: Message) -> bool:
    return validate_text_input(message)

def validate_technologies(message: Message) -> bool:
    return validate_text_input(message)

def validate_consent(callback_data: str) -> bool:
    return callback_data == "consent_yes"