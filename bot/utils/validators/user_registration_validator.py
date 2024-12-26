import re
from aiogram.types import Message, Contact

def validate_text_input(message: Message, max_length: int = 4000) -> bool:
    """
    Validates if the input is a valid text message within the allowed length.
    """
    if not message.text or len(message.text) > max_length:
        return False
    return True

def validate_regex(message: Message, pattern: str) -> bool:
    """
    Validates if the input matches the provided regex pattern.
    """
    if not message.text or not re.match(pattern, message.text):
        return False
    return True

def validate_contact_input(message: Message) -> bool:
    """
    Validates if the input is a valid contact message.
    """
    if not isinstance(message.contact, Contact):
        return False
    return True

def validate_age(message: Message) -> bool:
    """
    Validates if the age is a number between 10 and 100.
    """
    if not message.text.isdigit():
        return False
    age = int(message.text)
    return 10 <= age <= 100

# def validate_university(message: Message) -> bool:
#     """
#     Validates if the university name is one of the accepted options.
#     """
#     valid_universities = {"НУЛП", "ЛНУ", "УКУ", "КПІ", "КНУ", "Ще в школі", "Вже закінчив(-ла)"}
#     return message.text in valid_universities

def validate_course(message: Message) -> bool:
    """
    Validates if the course is a valid number from 1 to 5.
    """
    valid_courses = {"Перший", "Другий", "Третій", "Четвертий", "На магістартурі", "Нічого з переліченого"}
    return message.text in valid_courses

def validate_email(message: Message) -> bool:
    """
    Validates if the input is a valid email address.
    """
    pattern = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
    return validate_regex(message, pattern)

def validate_it_experience(message: Message) -> bool:
    """
    Validates if the IT experience is one of the accepted options.
    """
    valid_responses = {"Так", "Ні", "Планую"}
    return message.text in valid_responses

def validate_source(message: Message) -> bool:
    """
    Validates if the input is a valid source (accepting any text input).
    """
    return validate_text_input(message)

def validate_technologies(message: Message) -> bool:
    """
    Validates if the technologies input is valid (accepting any text input).
    """
    return validate_text_input(message)

def validate_consent(callback_data: str) -> bool:
    """
    Validates if the user has agreed to the consent.
    """
    return callback_data == "consent_yes"