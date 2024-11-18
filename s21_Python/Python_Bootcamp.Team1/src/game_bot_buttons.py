from aiogram.types import KeyboardButton  # type: ignore
from typing import List, Dict

# CREATE PERSONAGE
CREATE_PROT: str = "Создать персонажа! 🙋‍♂️"
CREATE_PROT_BTN: KeyboardButton = KeyboardButton(text=CREATE_PROT)

PROT_NAME: str = "Ввести имя 🪪"
PROT_NAME_BTN: KeyboardButton = KeyboardButton(text=PROT_NAME)

CHANGE_NAME: str = "Изменить имя 🔄"
CHANGE_NAME_BTN: KeyboardButton = KeyboardButton(text=CHANGE_NAME)

PROT_CLASS: str = "Выбрать класс 👥"
PROT_CLS_BTN: KeyboardButton = KeyboardButton(text=PROT_CLASS)

PROT_ICO: str = "Выбрать внешность 🧑🏻"
PROT_ICO_BTN: KeyboardButton = KeyboardButton(text=PROT_ICO)

CHANGE_ICO: str = "Изменить внешность 🔄"
CHANGE_ICO_BTN: KeyboardButton = KeyboardButton(text=CHANGE_ICO)

CHANGE_CLS: str = "Изменить класс 🔄"
CHANGE_CLS_BTN: KeyboardButton = KeyboardButton(text=CHANGE_CLS)

GENERATE: str = "Сгенерировать 🤖"
GENERATE_BTN: KeyboardButton = KeyboardButton(text=GENERATE)

COMPLETE: str = "Завершить создание ✔️"
COMPLETE_BTN: KeyboardButton = KeyboardButton(text=COMPLETE)

START: str = "Начать игру! 🎮"
START_GAME_BTN: KeyboardButton = KeyboardButton(text=START)

# BACKS
BACK: str = "Назад 🔙"
BACK_BTN: KeyboardButton = KeyboardButton(text=BACK)

LEAVE: str = "Уйти 👋"
LEAVE_BTN: KeyboardButton = KeyboardButton(text=LEAVE)

EXIT: str = "Выйти 👣"
EXIT_BTN: KeyboardButton = KeyboardButton(text=EXIT)

# SAVE-LOAD
SAVE: str = "Сохраниться 💾"
SAVE_BTN: KeyboardButton = KeyboardButton(text=SAVE)

QUICK_SAVE: str = "Быстрое сохранение 💽"
QUICK_SAVE_BTN: KeyboardButton = KeyboardButton(text=QUICK_SAVE)

LOAD: str = "Загрузить игру 📖"
LOAD_BTN: KeyboardButton = KeyboardButton(text=LOAD)

QUICK_LOAD: str = "Быстрая загрузка ⏮"
QUICK_LOAD_BTN: KeyboardButton = KeyboardButton(text=QUICK_LOAD)

REMOVE_SAVE: str = "Удалить сохранение 🗑"
REMOVE_SAVE_BTN: KeyboardButton = KeyboardButton(text=REMOVE_SAVE)


BTNS_MEAN: Dict[str, str] = {
    "attack": "🗡",
    "talk": "💬",
    "whereami": "🧭",
    "inventory": "💼",
    "saves": "📜",
    "up": "⬆️",
    "down": "⬇️",
    "left": "⬅️",
    "right": "➡️",
}

DIR_BTNS_MEAN: Dict[str, str] = {
    "North": "Север ❄️",
    "South": "Юг ☀️",
    "East": "Восток 🌄",
    "West": "Запад 🤠",
    "Begining": "Бухта встреч 🅱",
}

NORTH_BTNS_MEAN: Dict[str, int] = {
    "🏔 Трактир на пристани": 2,
    "🏞 Залив серебряных ракушек": 3,
    "🏕 Сторожки в бору": 4,
}

SOUTH_BTNS_MEAN: Dict[str, int] = {
    "🏖 Банановый остров": 5,
    "🏜 Золотые закаты": 6,
    "🏝 Коралловый грот": 7,
}

EAST_BTNS_MEAN: Dict[str, int] = {
    "🏙 Пески востока": 8,
    "🏞 Зеленая лагуна": 9,
    "🏕 Базарные переулки": 10,
}

WEST_BTNS_MEAN: Dict[str, int] = {
    "🏞 Долина озёр": 11,
    "🏔 Ореховый лес": 12,
    "🏕 Птичий полуостров": 13,
}

# TALK
TALK_WITH: str = "Поговорить 💬"
TALK_WITH_BTN: KeyboardButton = KeyboardButton(text=TALK_WITH)

TRADE: str = "Торговать 🫰"
TRADE_BTN: KeyboardButton = KeyboardButton(text=TRADE)

BUY: str = "Меню покупки 📉"
BUY_BTN: KeyboardButton = KeyboardButton(text=BUY)

SELL: str = "Меню продажи 📈"
SELL_BTN: KeyboardButton = KeyboardButton(text=SELL)

DONE: str = "Готово 🤝"
DONE_BTN: KeyboardButton = KeyboardButton(text=DONE)

INSPECT: str = "Осмотреть 👀"
INSPECT_BTN: KeyboardButton = KeyboardButton(text=INSPECT)


# INVENTORY
THROW_OUT: str = "Выбросить 🚮"
THROW_OUT_BTN: KeyboardButton = KeyboardButton(text=THROW_OUT)

ALL: str = "Всё"
ALL_BTN: KeyboardButton = KeyboardButton(text=ALL)

USE: str = "Использовать ⚒️"
USE_BTN: KeyboardButton = KeyboardButton(text=USE)

CHOOSE_WEAPON: str = "Сменить оружие ⚔️"
CHOOSE_WEAPON_BTN: KeyboardButton = KeyboardButton(text=CHOOSE_WEAPON)

CHOOSE_ARMOR: str = "Сменить одежду 🛡"
CHOOSE_ARMOR_BTN: KeyboardButton = KeyboardButton(text=CHOOSE_ARMOR)

SHOW_QUESTS: str = "Показать квесты 📝"
SHOW_QUESTS_BTN: KeyboardButton = KeyboardButton(text=SHOW_QUESTS)


# ATTACK

ESCAPE: str = "Попробовать сбежать 💨"
ESCAPE_BTN: KeyboardButton = KeyboardButton(text=ESCAPE)

LOOT: str = "Забрать снаряжение ✊"


def get_game_buttons() -> List[List[KeyboardButton]]:
    """Makes the 3 lines of buttons to game control

    Returns
    -------
    List[List[KeyboardButton]]
        The list of buttons for multiline keyboard
    """

    first_row = [
        KeyboardButton(text=BTNS_MEAN["attack"]),
        KeyboardButton(text=BTNS_MEAN["up"]),
        KeyboardButton(text=BTNS_MEAN["talk"]),
    ]
    second_row = [
        KeyboardButton(text=BTNS_MEAN["left"]),
        KeyboardButton(text=BTNS_MEAN["inventory"]),
        KeyboardButton(text=BTNS_MEAN["right"]),
    ]
    third_row = [
        KeyboardButton(text=BTNS_MEAN["whereami"]),
        KeyboardButton(text=BTNS_MEAN["down"]),
        KeyboardButton(text=BTNS_MEAN["saves"]),
    ]
    return [first_row, second_row, third_row]


def get_direction_buttons() -> List[List[KeyboardButton]]:
    """Makes buttons for directions and back button

    Returns
    -------
    List[List[KeyboardButton]]
        The list of buttons for multiline keyboard
    """

    rows: List[List[KeyboardButton]] = []
    rows.append(
        [
            KeyboardButton(text=" "),
            KeyboardButton(text=DIR_BTNS_MEAN["North"]),
            KeyboardButton(text=" "),
        ]
    )
    rows.append(
        [
            KeyboardButton(text=DIR_BTNS_MEAN["West"]),
            KeyboardButton(text=DIR_BTNS_MEAN["Begining"]),
            KeyboardButton(text=DIR_BTNS_MEAN["East"]),
        ]
    )
    rows.append(
        [
            KeyboardButton(text=" "),
            KeyboardButton(text=DIR_BTNS_MEAN["South"]),
            KeyboardButton(text=" "),
        ]
    )
    rows.append([BACK_BTN])
    return rows


def get_north_buttons() -> List[KeyboardButton]:
    """North locations buttons

    Returns
    -------
    List[KeyboardButton]
        The list of north locations buttons
    """

    return [KeyboardButton(text=i) for i in NORTH_BTNS_MEAN]


def get_south_buttons() -> List[KeyboardButton]:
    """South locations buttons

    Returns
    -------
    List[KeyboardButton]
        The list of south locations buttons
    """

    return [KeyboardButton(text=i) for i in SOUTH_BTNS_MEAN]


def get_east_buttons() -> List[KeyboardButton]:
    """East locations buttons

    Returns
    -------
    List[KeyboardButton]
        The list of east locations buttons
    """

    return [KeyboardButton(text=i) for i in EAST_BTNS_MEAN]


def get_west_buttons() -> List[KeyboardButton]:
    """West locations buttons

    Returns
    -------
    List[KeyboardButton]
        The list of west locations buttons
    """

    return [KeyboardButton(text=i) for i in WEST_BTNS_MEAN]


GAME_BTNS = get_game_buttons()
DIR_BTNS = get_direction_buttons()
NORTH_BTNS = get_north_buttons()
SOUTH_BTNS = get_south_buttons()
EAST_BTNS = get_east_buttons()
WEST_BTNS = get_west_buttons()
ALL_DIRS_MEAN = {
    **NORTH_BTNS_MEAN,
    **SOUTH_BTNS_MEAN,
    **EAST_BTNS_MEAN,
    **WEST_BTNS_MEAN,
}
