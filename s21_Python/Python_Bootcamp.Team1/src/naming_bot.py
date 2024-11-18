"""The module is a Telegram bot for generating names in the game

Module requires os and load_dotenv to load environment variables from
the .env file, logging - to log the program process, json - to load the
name database, random - to randomize the naming, asyncio and aiogram -
to implement the asynchronious Telegram bot
"""

import os
from dotenv import load_dotenv  # type: ignore
import logging
import json
import random
import asyncio
from aiogram import Bot, Dispatcher, F, Router  # type: ignore
from aiogram.filters import CommandStart  # type: ignore
from aiogram.types import (  # type: ignore
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext  # type: ignore
from aiogram.fsm.state import State, StatesGroup  # type: ignore
from typing import Tuple, Dict, List, Any


def get_token(var: str) -> str:
    """Getting Telegram-bot token from environment variable

    Parameters
    ----------
    var : str
        environment variable

    Returns
    -------
    str
        bot token

    Raises
    ------
    ValueError
        If environment variable did not set
    """

    token: str = ""
    temp: str | None = os.getenv(var)
    if temp is None:
        raise ValueError(f"{var} environment variable did not set")
    token = temp
    return token


def get_dicts() -> (
    Tuple[Dict[str, Dict[str, List[str]]], Dict[str, Dict[str, List[str]]]]
):
    """Import dictionaries from json file

    Returns
    -------
    Tuple[Dict[str, Dict[str, List[str]], Dict[str, Dict[str, List[str]]]
        The character and item names dictionaries

    Raises
    ------
    ValueError
        If environment variable did not set
    """

    filename: str = ""
    temp: str | None = os.getenv("NAMING_JSON")
    if temp is None:
        raise ValueError("NAMING_JSON environment variable did not set")
    filename = temp
    with open(filename, "r") as file:
        dicts: Dict[str, Dict[str, Dict[str, List[str]]]] = json.load(file)
    return dicts["Персонаж"], dicts["Вещь"]


dp = Dispatcher()
form_router = Router()
load_dotenv()
PERSONS, ITEMS = get_dicts()

MENU: Dict[str, str] = {"pers": "Персонаж", "item": "Вещь"}
BACK: str = "Назад"

MENU_BTNS: List[KeyboardButton] = [
    KeyboardButton(text=MENU["pers"]),
    KeyboardButton(text=MENU["item"]),
]

BACK_BTN = KeyboardButton(text=BACK)


class Form(StatesGroup):
    main = State()
    character_name = State()
    item_name = State()
    current_state = State()


async def create_keyboard(buttons: Any, width=1) -> ReplyKeyboardMarkup:
    """Creates keyboard from buttons

    Parameters
    ----------
    buttons : List[Any]
        The list of KeyboardButton

    Returns
    -------
    ReplyKeyboardMarkup
        The keyboard
    """
    keyboard = buttons if any(type(x) is list for x in buttons) else [buttons]
    return ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=width, keyboard=keyboard
    )


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    """/start command handler.

    Sets the initial state of the bot and displays the main menu.

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed.
    state : FSMContext
        FSM state context.
    """

    await state.set_state(Form.main)
    await state.update_data(current_state="Main")
    await message.answer(
        "Добро пожаловать! Выберите категорию:",
        reply_markup=await create_keyboard(MENU_BTNS),
    )


@dp.message(F.text == BACK)
async def back(message: Message, state: FSMContext):
    """Returns the user one level back depending on the current state.

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed.
    state : FSMContext
        FSM state context.
    """

    data: Dict[str, Any] = await state.get_data()
    cur_state: str | None = data.get("current_state")
    if cur_state in MENU.values():
        await state.set_state(Form.main)
        await state.update_data(current_state="Main")
        await message.answer(
            "Выберите категорию:",
            reply_markup=await create_keyboard(MENU_BTNS),
        )
    else:
        await start(message, state)


@form_router.message(Form.main)
@dp.message(lambda message: message.text in MENU.values())
async def menu_handler(msg: Message, state: FSMContext):
    """The main menu includes the user's choice between character and items

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed.
    state : FSMContext
        FSM state context.
    """

    data: Dict[str, Any] = await state.get_data()
    cur_state: str | None = data.get("current_state")
    if cur_state == MENU["pers"] or msg.text == MENU["pers"]:
        await choose_category(
            msg, Form.character_name, state, PERSONS.keys(), MENU["pers"]
        )
    elif cur_state == MENU["item"] or msg.text == MENU["item"]:
        await choose_category(
            msg, Form.item_name, state, ITEMS.keys(), MENU["item"]
        )


async def choose_category(
    msg: Message, form: State, state: FSMContext, keys: Any, category: str
) -> None:
    """Show category form

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed.
    form : State
        The form of category
    state : FSMContext
        FSM state context.
    keys : Any
        The list of submenu categories
    category : str
        The name of category
    """

    await state.set_state(form)
    await state.update_data(current_state=category)
    keyboard: List[KeyboardButton] = [KeyboardButton(text=k) for k in keys]
    await msg.answer(
        f'Выберите из категории "{category}":',
        reply_markup=await create_keyboard(keyboard + [BACK_BTN]),
    )


@form_router.message(Form.character_name or Form.item_name)
@dp.message(lambda msg: msg.text in list(PERSONS.keys()) + list(ITEMS.keys()))
async def generate_menu_handler(msg: Message, state: FSMContext):
    """Submenu for generating names from the selected category

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed.
    state : FSMContext
        FSM state context.
    """

    data: Dict[str, Any] = await state.get_data()
    cur_state: str | None = data.get("current_state")
    keys: List[str] = []
    if cur_state == MENU["pers"]:
        if msg.text in PERSONS:
            cur_class: Dict[str, List[str]] = PERSONS[msg.text]
            name: str = create_name(cur_class["Имя"], cur_class["Фамилия"])
            await state.update_data(character_name=name)
            keys = list(PERSONS.keys())
    elif cur_state == MENU["item"]:
        if (
            msg.text in ITEMS
            and "Атрибут" in ITEMS[msg.text]
            and "Тип" in ITEMS[msg.text]
        ):
            name = create_name(
                ITEMS[msg.text]["Атрибут"], ITEMS[msg.text]["Тип"]
            )
            data = await state.get_data()
            items: Dict[str, str] | None = data.get("item_name")
            if items:
                items[msg.text] = name
            else:
                items = {msg.text: name}
            await state.update_data(item_name=items)
            keys = list(ITEMS.keys())
    keyboard: List[KeyboardButton] = [KeyboardButton(text=k) for k in keys]
    await msg.answer(
        f'Сгенерированное имя для "{msg.text}": {name}',
        reply_markup=await create_keyboard(keyboard + [BACK_BTN]),
    )


def create_name(vars1: List[str], vars2: List[str]) -> str:
    """Generates a name by randomly choosing from 2 lists

    Parameters
    ----------
    vars1 : List[str]
        The first list
    vars2 : List[str]
        The second list

    Returns
    -------
    str
        The generated name
    """

    return f"{random.choice(vars1)} {random.choice(vars2)}"


async def main(var: str) -> None:
    """Starts the bot's event processing using aiogram.

    Parameters
    ----------
    var : str
        The environment variable
    """

    bot = Bot(get_token(var))
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    bot_token: str = "NAMING_BOT_TOKEN"
    asyncio.run(main(bot_token))
