import time

user_last_requests = {}

def is_duplicate_request(user_id: int, message_text: str, cooldown: int = 3) -> bool:
    current_time = time.time()

    if user_id in user_last_requests:
        last_text, last_time = user_last_requests[user_id]

        if last_text == message_text and (current_time - last_time) < cooldown:
            return True

    user_last_requests[user_id] = (message_text, current_time)
    return False
