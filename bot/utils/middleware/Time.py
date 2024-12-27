import time

# Глобальний кеш для зберігання останніх запитів
user_last_requests = {}

def is_duplicate_request(user_id: int, message_text: str, cooldown: int = 3) -> bool:
    """
    Перевіряє, чи є запит користувача дублікатом.
    :param user_id: ID користувача
    :param message_text: Текст повідомлення
    :param cooldown: Час у секундах, протягом якого запити вважаються дублікатами
    :return: True, якщо запит є дублікатом, False інакше
    """
    current_time = time.time()

    # Перевіряємо, чи є дані для користувача
    if user_id in user_last_requests:
        last_text, last_time = user_last_requests[user_id]

        # Якщо текст і час відповідають умовам дублювання
        if last_text == message_text and (current_time - last_time) < cooldown:
            return True

    # Оновлюємо кеш для цього користувача
    user_last_requests[user_id] = (message_text, current_time)
    return False
