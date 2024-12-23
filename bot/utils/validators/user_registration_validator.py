import re

def validate_email(email: str) -> bool:
    """
    Перевірка коректності email.
    """
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None

def validate_age(age: str) -> bool:
    """
    Перевірка віку як цілого числа.
    """
    return age.isdigit() and 10 <= int(age) <= 100

def validate_course(course: str) -> bool:
    """
    Перевірка правильності курсу (1-5).
    """
    return course.isdigit() and 1 <= int(course) <= 5

def validate_university(university: str) -> bool:
    """
    Перевірка правильності університету.
    """
    return university in ["НУЛП", "ЛНУ"]
