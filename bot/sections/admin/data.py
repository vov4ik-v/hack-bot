from aiogram.filters.callback_data import CallbackData


class TeamCallbackData(CallbackData, prefix="team"):
    action: str
    team_id: str


ADMIN_WELCOME = "Вітаю в адмінці"
ADMIN_EXIT = "Ви вийшли з адмінки. Повертаємось до звичайного меню..."
STAGE_SELECTION_PROMPT = "Оберіть стадію, на яку бажаєте переключитись:"
STAGE_SELECTION_CANCEL = "Зміну стадії скасовано."
STAGE_SELECTION_INVALID = "Неправильно вибрана стадія. Спробуйте ще раз або скасуйте."
STAGE_SWITCHED = "Секцію переключено на: {}"
BROADCAST_PROMPT = "Оберіть категорію для розсилки:"
BROADCAST_CANCEL = "Розсилку скасовано."
BROADCAST_COMPLETE = "Розсилку завершено. Категорія: {}."
TEAM_SELECTION_PROMPT = "Оберіть команду для подальших дій:"
TEAM_NOT_FOUND = "Команду не знайдено або вже видалено."
TEAM_SELECTED = "Обрано команду: {}\nОберіть дію:"
NO_TEAMS_AVAILABLE = "Немає доступних команд."
INVALID_TEAM_ID = "Неправильний формат ідентифікатора команди."
INVALID_DATA_FORMAT = "Невірний формат даних."
UNKNOWN_ACTION = "Невідома дія"