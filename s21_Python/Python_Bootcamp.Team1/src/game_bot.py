"""The module implements the game logic on the telegram bot engine

Module requires:
- asyncio and aiogram: For asynchronous communication with the
Telegram API.
- dotenv: To load environment variables from a .env file.
- logging: For logging errors and debugging purposes.
- uuid4: To generate unique identifiers for protagonists.
- time: To add timestamps to saves.
- copy: For deep copying classes and lists.
- random: To generate initial parameters for protagonist, add сhances
to some events, for init minigame.
- sqlalchemy: To manage game progress in a PostgreSQL database.
- naming_bot: For generating names for protagonists, to build Telegram
keyboard and load environment variables.
- characters_classes: Contains the character definitions and core game
logic of interaction.
- load_data: Needs to connecton for database
- load_all: Loads data from the PostgreSQL database to fill characters
and locations
- fill_data: Initializes the database if empty.
- tables: For querying specific tables.
- game_bot_buttons: Contains all interactive game buttons.
"""

import asyncio
from aiogram import Dispatcher, Bot, F, Router  # type: ignore
from aiogram.filters import CommandStart  # type: ignore
from aiogram.types import (  # type: ignore
    Message,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext  # type: ignore
from aiogram.fsm.state import State, StatesGroup  # type: ignore
from dotenv import load_dotenv  # type: ignore
import logging
import argparse
from uuid import uuid4
import time
import copy
import random as r
from sqlalchemy.orm import Session  # type: ignore
from naming_bot import create_keyboard, get_token, create_name, PERSONS
import character_classes as c
from load_data import get_session, create_db_and_user
from load_all import load_all
import fill_data as fd
from tables import (
    Save,
    Person,
    Person_Item,
    Person_Weapon,
    Person_Quest,
    Person_BuffItem,
)
import game_bot_buttons as b
from typing import Dict, List, Union, Any, Optional, Tuple


load_dotenv()
form_router = Router()


class Form(StatesGroup):
    """States before the start of the game

    "Создать персонажа" | Form.create
        "Ввести имя"
            "Теперь введите имя: | Form.input_name
                "Изменить имя"
                "Назад"
            "Назад"
        "Выбрать класс"
            "Изменить класс" | Form.choose_class
            "Назад"
        "Сгенерировать" | Form.generate
        "Завершить создание"
            "Начать игру" | Form.start_game
            "Изменить имя"
            "Изменить класс"
    "Загрузить игру" | Form.create
    """

    start = State()
    create = State()
    input_name = State()
    choose_class = State()
    choose_appearance = State()
    generate = State()
    start_game = State()
    null = State()


class GameStates(StatesGroup):
    """States that arise during the game"""

    run = State()
    attack = State()
    attack_enemy = State()
    talk = State()
    talk_with = State()
    dialogue = State()
    inventory = State()
    show_quests = State()
    trade = State()
    trade_list = State()
    trade_item = State()
    throw = State()
    reduce_item = State()
    use = State()
    choose_weapon = State()
    choose_armor = State()
    whereami = State()
    save_menu = State()
    save = State()
    load_start = State()
    load = State()
    remove_save_menu = State()
    remove_save = State()
    die = State()
    choose_location = State()
    choose_sub_loc = State()
    start_game = State()
    game_go = State()


DATA: Dict[str, Any] = {
    "init": {
        "name": "",
        "class_name": "",
        "appearance": "",
        "appearances": [
            "🙎‍♂️",
            "🧑🏻",
            "👨🏼",
            "🥷",
            "👨🏻‍🦰",
            "👳🏼‍♂️",
            "💂🏼",
            "👲🏼",
            "🤴",
        ],
    },
    "args": None,
    "hero": c.Protagonist("null"),
    "npcs": [],
    "enemies": [],
    "fields": [],
    "map_free": ["🟩", "🟨", "⬜", "🟦", "🟫", "🟧"],
    "traces": {},
    "pursuit": [],
    "union": [],
    "items_duration": [],
}


@form_router.message(F.text.in_([b.BACK, b.LEAVE]))
async def back(message: Message, state: FSMContext):
    """Back and leave buttons handle

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    form_backs: Dict[State, State] = {
        Form.create: Form.start,
        Form.input_name: Form.create,
        Form.choose_class: Form.create,
        Form.choose_appearance: Form.create,
        GameStates.run: GameStates.run,
        GameStates.attack: GameStates.run,
        GameStates.talk: GameStates.run,
        GameStates.talk_with: GameStates.talk,
        GameStates.dialogue: GameStates.talk_with,
        GameStates.inventory: GameStates.run,
        GameStates.show_quests: GameStates.inventory,
        GameStates.trade: GameStates.run,
        GameStates.trade_list: GameStates.trade,
        GameStates.trade_item: GameStates.trade_list,
        GameStates.throw: GameStates.inventory,
        GameStates.reduce_item: GameStates.inventory,
        GameStates.use: GameStates.inventory,
        GameStates.choose_weapon: GameStates.run,
        GameStates.choose_armor: GameStates.run,
        GameStates.whereami: GameStates.run,
        GameStates.choose_location: GameStates.run,
        GameStates.choose_sub_loc: GameStates.choose_location,
        GameStates.save_menu: GameStates.run,
        GameStates.remove_save: GameStates.run,
        GameStates.remove_save_menu: GameStates.run,
        GameStates.save: GameStates.save_menu,
        GameStates.load_start: Form.start,
        GameStates.load: GameStates.run,
    }

    cur_state: Optional[str] = await state.get_state()
    checked_state: State = Form.null
    if cur_state:
        states = [s for s in form_backs if s == cur_state]
        if states:
            checked_state = states[0]
    back_state = form_backs.get(checked_state, None)
    if back_state is None:
        await message.answer("Назад дороги нет")
    else:
        if checked_state == GameStates.trade:
            await clean_list_trade(state)
        await state.set_state(back_state)
        await FORM_FUNCS[back_state](message, state)


@form_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    """Bot start message

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(Form.create)
    st_data: Dict[str, Any] = await state.get_data()
    if st_data:
        await state.update_data({})
    text: str = "Добро пожаловать, герой!🤠\nСоздай персонажа и начинай игру⛵️"
    keys = [b.CREATE_PROT_BTN, b.LOAD_BTN]
    await message.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.create, F.text == b.PROT_NAME)
async def invite_to_input_name(message: Message, state: FSMContext):
    """Waiting for name input

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(Form.input_name)
    text: str = "Теперь введите имя: 🔤"
    keys = [b.BACK_BTN]
    await message.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.create, F.text == b.PROT_CLASS)
async def invite_to_choose_class(message: Message, state: FSMContext):
    """Waiting for class selection

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(Form.choose_class)
    text: str = "Выберите класс 👥"
    keys = [KeyboardButton(text=pc) for pc in c.PLAYABLE_CLS] + [b.BACK_BTN]
    await message.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.create, F.text == b.PROT_ICO)
async def invite_to_choose_appearance(message: Message, state: FSMContext):
    """Waiting for class selection

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(Form.choose_appearance)
    text: str = "Выберите внешность 🧑🏻"
    keys = [KeyboardButton(text=i) for i in DATA["init"]["appearances"]] + [
        b.BACK_BTN
    ]
    await message.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.create, F.text == b.GENERATE)
async def generate_protagonist(message: Message, state: FSMContext):
    """Generate name and class of protagonist

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    values: List[int] = list(c.PLAYABLE_CLS.values())
    class_id = c.r.randint(min(values), max(values))
    init = DATA["init"]
    init["class_name"] = "".join(
        [k for k, v in c.PLAYABLE_CLS.items() if v == class_id]
    )
    key: str = init["class_name"].split()[0]
    init["name"] = create_name(PERSONS[key]["Имя"], PERSONS[key]["Фамилия"])
    init["appearance"] = r.choice(init["appearances"])
    text: str = (
        f"Сгенерированное имя: {init['name']}, класс "
        f"{init['class_name']} и внешность {init['appearance']}"
    )
    keys = [b.GENERATE_BTN, b.COMPLETE_BTN, b.BACK_BTN]
    await message.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.create, F.text == b.COMPLETE)
async def create_protagonist(message: Message, state: FSMContext):
    """Creates the protagonist

    Waits for his characteristics to change, or starts the game

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context

    Raises
    ------
    ValueError
        If the name or class of protagonist did not set
    """

    try:
        await state.set_state(Form.start_game)
        global DATA
        error: str = ""
        init = DATA["init"]
        if (
            not len(init["name"])
            or not len(init["class_name"])
            or not len(init["appearance"])
        ):
            if not len(init["name"]):
                error = "Имя не задано"
            elif not len(init["class_name"]):
                error = "Класс не задан"
            elif not len(init["appearance"]):
                error = "Внешность не задана"
            raise ValueError(error)
        DATA["hero"] = c.Protagonist(
            name=init["name"],
            class_id=c.PLAYABLE_CLS[init["class_name"]],
            id=str(uuid4()),
        )
        text = (
            f"Имя персонажа: {init['name']}\n"
            f"Класс: {init['class_name']}\n"
            f"Внешность: {init['appearance']}\n"
            f"ID: {DATA['hero'].id}"
        )
        keys = [
            b.CHANGE_NAME_BTN,
            b.CHANGE_CLS_BTN,
            b.CHANGE_ICO_BTN,
            b.START_GAME_BTN,
        ]
        await message.answer(text, reply_markup=await create_keyboard(keys))
    except ValueError:
        await state.set_state(Form.create)
        text = f"Пожалуйста введите все необходимые данные: {error} ❌"
        await message.answer(text)


@form_router.message(Form.create, F.text == b.LOAD)
async def init_load_game(message: Message, state: FSMContext):
    """Load game from start the game

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.load_start)
    text: str = "Введите ID героя, которого хотите загрузить"
    await state.update_data(is_init_load=True)
    keys = [b.BACK_BTN]
    await message.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.load_start)
async def load_start(msg: Message, state: FSMContext):
    """Loads game proccess from start

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    if inp:
        DATA["hero"].id = inp
        args: Optional[argparse.Namespace] = parsing_arguments()
        DATA["args"] = args
        await load_choose(msg, state)


@form_router.message(Form.create, F.text == b.CREATE_PROT)
async def start_create(message: Message, state: FSMContext):
    """Main menu of creating protagonist

    Parameters
    ----------
    message : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    init = DATA["init"]
    text: str = (
        f"👨‍🔧 Создание персонажа\nИмя: {init['name']}\nКласс: "
        f"{init['class_name']}\nВнешность: {init['appearance']}"
    )
    await state.update_data(create=text)
    keys = [
        b.PROT_NAME_BTN,
        b.PROT_CLS_BTN,
        b.PROT_ICO_BTN,
        b.GENERATE_BTN,
        b.COMPLETE_BTN,
    ]
    keys = split_buttons(keys)
    await message.answer(text, reply_markup=await create_keyboard(keys))


def split_buttons(keys: List[Any]) -> List[Any]:
    """Split keys into several rows

    Parameters
    ----------
    keys : List[Any]
        Given keys

    Returns
    -------
    List[Any]
        Keys in several list rows
    """

    vision_threshold: int = 4
    temp: List[List[KeyboardButton]] = [[]]
    if len(keys) > vision_threshold:
        i = 1
        for key in keys:
            if i % vision_threshold == 0:
                temp.append([])
            temp[i // vision_threshold].append(key)
            i += 1
    else:
        temp = [keys]
    temp.append([b.BACK_BTN])
    keys = temp
    return keys


@form_router.message(Form.input_name)
async def accept_name(msg: Message, state: FSMContext):
    """Check name input

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    if inp == b.BACK:
        await back(msg, state)
    elif inp == b.CHANGE_NAME:
        await invite_to_input_name(msg, state)
    else:
        DATA["init"]["name"] = inp
        text = f"Имя персонажа: {inp} 🪪"
        keys = [b.CHANGE_NAME_BTN, b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.choose_class)
async def accept_class(msg: Message, state: FSMContext):
    """Check class input

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    if inp == b.BACK:
        await back(msg, state)
    elif inp == b.CHANGE_CLS:
        await invite_to_choose_class(msg, state)
    elif inp:
        class_id = c.PLAYABLE_CLS.get(inp, None)
        if class_id is not None:
            global DATA
            DATA["init"]["class_name"] = inp
        text: str = f"Класс персонажа: {inp}"
        keys = [b.CHANGE_CLS_BTN, b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.choose_appearance)
async def accept_appearance(msg: Message, state: FSMContext):
    """Check appearance input

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    if inp == b.BACK:
        await back(msg, state)
    elif inp == b.CHANGE_ICO:
        await invite_to_choose_appearance(msg, state)
    elif inp:
        text: str = ""
        if inp in DATA["init"]["appearances"]:
            DATA["init"]["appearance"] = inp
            text = f"Внешность персонажа: {inp}"
        else:
            text = "Внешность не подходит"
        keys = [b.CHANGE_ICO_BTN, b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(Form.start_game)
async def start_game(msg: Message, state: FSMContext):
    """Change protagonist characteristics or start game

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    if inp == b.CHANGE_NAME:
        await invite_to_input_name(msg, state)
    elif inp == b.CHANGE_CLS:
        await invite_to_choose_class(msg, state)
    elif inp == b.CHANGE_ICO:
        await invite_to_choose_appearance(msg, state)
    elif inp == b.START:
        args = parsing_arguments()
        global DATA
        init = DATA["init"]
        if init["appearance"] is None:
            raise ValueError("Внешность не выбрана")
        DATA["hero"].appearance = init["appearance"]
        DATA = load_all(DATA, args=args, is_init_load=True)
        await state.update_data(start_time=time.time())
        if DATA["npcs"] is None or DATA["enemies"] is None:
            raise ValueError("NPC не загружены")
        if DATA["phrases"] is None:
            raise ValueError("Диалоги не загружены")
        await state.set_state(GameStates.run)
        text = "Волны хлещут о берег... 🏝"
        keys = [KeyboardButton(text="Осмотреться")]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


# GameState FSM


@form_router.message(
    GameStates.run,
    F.text.in_(
        [
            b.BTNS_MEAN["up"],
            b.BTNS_MEAN["down"],
            b.BTNS_MEAN["left"],
            b.BTNS_MEAN["right"],
        ]
    ),
)
async def choose_direction(msg: Message, state: FSMContext):
    """Movement to the cardinal points

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    if msg.text:
        hero = DATA["hero"]
        lid: int = hero.location_id
        field: List[List[str]] = DATA["fields"][lid - 1]
        map_free = DATA["map_free"] + DATA["init"]["appearances"]
        check = go_handle(hero, msg.text, field, map_free)
        text: str = ""
        if check == c.Position.CORRECT:
            text += "Топ-топ"
            text += (
                items_duration_handle(hero) if DATA["items_duration"] else ""
            )
        else:
            text = "Туда не пройти"
        await msg.answer(
            text, reply_markup=await create_keyboard(b.GAME_BTNS, 3)
        )
        await npc_walking(msg, state, lid, field)


async def npc_walking(
    msg: Message, state: FSMContext, lid: int, field: List[List[str]]
) -> None:
    """NPC movement processing

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    lid : int
        The location ID
    field : List[str]
        The current location matrix
    """

    npcs = [
        npc for npc in DATA["npcs"] + DATA["enemies"] if npc.location_id == lid
    ]

    hero = DATA["hero"]
    map_free = DATA["map_free"] + DATA["init"]["appearances"]
    for npc in npcs:
        if npc in DATA["union"]:
            hero.union_handle(field, map_free, npc) if npc.hp > 0 else None
            continue

        chance: int = r.randint(0, 1)
        if chance and not npc.pursuit_time:
            direct: str = r.choice(
                [
                    b.BTNS_MEAN["up"],
                    b.BTNS_MEAN["down"],
                    b.BTNS_MEAN["left"],
                    b.BTNS_MEAN["right"],
                ]
            )
            go_handle(npc, direct, field, map_free)

        if npc.pursuit_time and npc.pursuit_time > 0:
            text: str = hero.pursuit_handle(
                npc, field, map_free, DATA["pursuit"]
            )
            if text:
                await msg.answer(text)
                await battle(msg, state, hero, [npc], npc)


def go_handle(
    person: Union[c.Protagonist, c.NPC],
    direction: str,
    field: List[List[str]],
    map_free: List[str],
) -> c.Position:
    """Checking the correctness of movement and the movement if success

    Parameters
    ----------
    person : Union[c.Protagonist, c.NPC]
        The person who moved
    direction: str
        Direction of movement
    field : List[str]
        The current location where the person in
    map_free : List[str]
        List of characters that person can stand on

    Returns
    -------
    c.Position
        Position correctness status
    """

    pos: c.Direction = person.whereami()
    new_dir: c.Direction = pos
    if direction == b.BTNS_MEAN["up"]:
        new_dir = c.Direction(pos.x, pos.y + 1)
    elif direction == b.BTNS_MEAN["down"]:
        new_dir = c.Direction(pos.x, pos.y - 1)
    elif direction == b.BTNS_MEAN["left"]:
        new_dir = c.Direction(pos.x - 1, pos.y)
    elif direction == b.BTNS_MEAN["right"]:
        new_dir = c.Direction(pos.x + 1, pos.y)
    check: c.Position = person.is_correct_pos(field, map_free, new_dir)
    if check == c.Position.CORRECT:
        person.go(new_dir)
    return check


def items_duration_handle(hero: c.Protagonist) -> str:
    """Drops boost effects if items duration ends

    Parameters
    ----------
    hero : c.Protagonist
        The protagonist of game

    Returns
    -------
    str
        The informational message about drop effect
    """

    text: str = ""
    removes: List[c.Item] = []
    for item in DATA["items_duration"]:
        if item.duration:
            item.duration -= 1
            is_used: bool = True
            if item.duration <= 0:
                removes.append(item)
                is_used = False
            if item.buff_reusable and is_used:
                text += "\n"
                if item.buff_parameter == c.ItemBuff.HP:
                    hero.heal(item.buff)
                    text += f"Ваши hp повысились на {item.buff}"
                elif item.buff_parameter == c.ItemBuff.DEFENSE:
                    hero.armor += item.buff
                    text += f"Ваша защита повысилась на {item.buff}"
                elif item.buff_parameter == c.ItemBuff.DAMAGE:
                    hero.weapon.dmg_min += item.buff
                    hero.weapon.dmg_max += item.buff
                    text += f"Ваш урон повысился на {item.buff}"

    for i in removes:
        DATA["items_duration"].remove(i)
        text += f"\nЭффект от {i.name} закончился"
        if i.buff_parameter == c.ItemBuff.DAMAGE:
            hero.weapon.dmg_min -= item.buff
            hero.weapon.dmg_max -= item.buff
        elif i.buff_parameter == c.ItemBuff.DEFENSE:
            hero.armor.buff -= item.buff
    return text


async def battle(
    msg: Message,
    state: FSMContext,
    hero: c.Protagonist,
    enemies_in_range: List[c.Enemy],
    enemy: Optional[c.Enemy],
) -> None:
    """Battle with enemy

    Possibly in alliance with union NPCs and against enemies who have
    heard the battle

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    hero : c.Protagonist
        The protagonist of game
    enemies_in_range : List[c.Enemy]
        The enemies within the protagonists attack range
    enemy : Optional[c.Enemy]
        The enemy with whom the battle began
    """

    keys: List[KeyboardButton] = []
    text: str = hero.attack(enemy, DATA) if enemy else ""
    is_die: bool = False
    battle_mode: bool = True
    if c.Phrases.DEFEAT.value in text:
        is_die = True

    if not is_die and c.Phrases.ENEMY_DEFEAT.value in text:
        await loot_in_range(state, hero, enemies_in_range, keys, battle_mode)

    i: int = 0
    N: int = len(DATA["union"])
    while i < N and not is_die:
        npc = DATA["union"][i]
        if enemy and enemy.hp > 0:
            text += npc.attack(enemy, DATA)
        elif enemies_in_range:
            try:
                enemy = npc.choose_weakest(DATA, enemy)
                text += npc.attack(enemy, DATA)
            except Exception:
                if enemy and enemy.hp <= 0:
                    enemy = None

        i += 1

    if not is_die and c.Phrases.DEFEAT.value in text:
        is_die = True
    elif not is_die and c.Phrases.ENEMY_DEFEAT.value in text:
        await loot_in_range(state, hero, enemies_in_range, keys, battle_mode)

    if not is_die:
        text_part: str = await enemy_attack(
            state, hero, enemies_in_range, keys, enemy
        )
        if c.Phrases.DEFEAT.value in text:
            is_die = True
        else:
            text += text_part

    keys += get_keys_to_attack_enemies(enemies_in_range)
    keys += [KeyboardButton(text=f"{b.BTNS_MEAN['whereami']} Карта")]
    if enemies_in_range and DATA["pursuit"]:
        keys += [b.ESCAPE_BTN]
    else:
        keys += [b.LEAVE_BTN]
    (
        await msg.answer(
            text, parse_mode="HTML", reply_markup=await create_keyboard(keys)
        )
        if not is_die
        else await die(msg, state)
    )


async def enemy_attack(
    state: FSMContext,
    hero: c.Protagonist,
    enemies_in_range: List[c.Enemy],
    keys: List[KeyboardButton],
    enemy=None,
) -> str:
    """Enemies in range сounter attack

    Possibly in alliance with union NPCs and against enemies who have
    heard the battle

    Parameters
    ----------
    state : FSMContext
        FSM state context
    hero : c.Protagonist
        The protagonist of game
    enemies_in_range : List[c.Enemy]
        The enemies within the protagonists attack range
    keys: List[KeyboardButton]
        Telegram keyboard keys
    enemy : Optional[c.Enemy]
        The enemy with whom the battle began, by default None
    """

    if enemy:
        enemy_id = enemy.id
    else:
        enemy_id = ""
    text: str = ""
    attack_heard_range: int = 3
    is_die: bool = False
    i: int = 0
    N: int = len(DATA["enemies"])
    battle_mode: bool = True
    while i < N and not is_die:
        e = DATA["enemies"][i]
        if (
            e.id != enemy_id
            and hero.hp > 0
            and (
                e.is_in_range(hero, attack_heard_range)
                or any(
                    [
                        er.is_in_range(e, attack_heard_range)
                        for er in enemies_in_range
                        if er.id != e.id
                    ]
                )
            )
        ):
            if e.hp > 0:
                text += e.attack(hero, DATA)

                if c.Phrases.DEFEAT.value in text:
                    is_die = True
                elif c.Phrases.ENEMY_DEFEAT.value in text:
                    await loot_in_range(
                        state, hero, enemies_in_range, keys, battle_mode
                    )
                elif e not in enemies_in_range:
                    enemies_in_range.append(e)
            elif e in enemies_in_range:
                enemies_in_range.remove(e) if e in enemies_in_range else None
        i += 1

    return text


def get_keys_to_attack_enemies(enemies: List[c.Enemy]) -> List[KeyboardButton]:
    """Adds the enemies name within protagonists attack range to keys

    Parameters
    ----------
    enemies_in_range : List[c.Enemy]
        The enemies within the protagonists attack range

    Returns
    -------
    List[KeyboardButton]
        Telegram keyboard keys
    """

    keys = []
    for e in enemies:
        (
            keys.append(
                KeyboardButton(text=f"{b.BTNS_MEAN['attack']} {e.name}")
            )
            if e.hp > 0
            else None
        )
    return keys


@form_router.message(GameStates.run, F.text.contains(b.BTNS_MEAN["attack"]))
async def attack(msg: Message, state: FSMContext):
    """Attack menu - shows the characters could be attacked

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.attack)
    text: str = "Кого атаковать? 🗡"
    enemies_in_range = await get_enemies_in_range(state)
    keys = get_keys_to_attack_enemies(enemies_in_range)
    keys = split_buttons(keys)
    await state.update_data(npcs_lootable=[])
    await msg.answer(text, reply_markup=await create_keyboard(keys))


async def get_enemies_in_range(state: FSMContext) -> List[Any]:
    """Getting a list of enemies that are within protagonist's reach

    Parameters
    ----------
    state : FSMContext
        FSM state context

    Returns
    -------
    List[Any]
        List of enemies or in case of a corsair any characters
    """

    hero = DATA["hero"]
    enemies: List[c.Enemy] = DATA["enemies"].copy()
    talk_range: int = 2
    range: int = max(talk_range, hero.weapon.range)
    if hero.class_id == c.ClassID.CORSAIR:
        enemies += DATA["npcs"]
    enemies_in_range: List[c.Enemy] = [
        e
        for e in enemies
        if e.hp > 0 and hero.is_in_range(e, range)
    ]
    await state.update_data(enemies_in_range=enemies_in_range)
    return enemies_in_range


@form_router.message(GameStates.attack)
async def attack_handle(msg: Message, state: FSMContext):
    """Attacks certain enemy

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    hero: c.Protagonist = DATA["hero"]
    st_data: Dict[str, Any] = await state.get_data()
    enemies_in_range: List[c.Enemy] = st_data.get("enemies_in_range", [])
    keys: List[KeyboardButton] = []
    if inp and inp.startswith(b.LOOT):
        name: str = inp[inp.find("у ") + 2:]
        npcs_lootable = st_data.get("npcs_lootable", [])
        text = hero.loot(name, DATA, npcs_lootable)
        if enemies_in_range:
            keys += get_keys_to_attack_enemies(enemies_in_range)
            battle_mode = True
            await loot_in_range(
                state, hero, enemies_in_range, keys, battle_mode
            )
            keys += [KeyboardButton(text=f"{b.BTNS_MEAN['whereami']} Карта")]
            if DATA["pursuit"]:
                keys += [b.ESCAPE_BTN]
            else:
                keys += [b.LEAVE_BTN]
        else:
            keys = [b.LEAVE_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))
    elif inp and inp.startswith(b.BTNS_MEAN["whereami"]):
        await msg.answer(await show_map(msg, state))
    elif inp == b.ESCAPE:
        if r.randint(0, 1):
            await choose_action(msg, state)
        else:
            text = "Не удалось\n"
            part: str = await enemy_attack(state, hero, enemies_in_range, keys)
            text += part
            await msg.answer(text, parse_mode="HTML")
    elif inp and inp.startswith(b.BTNS_MEAN["attack"]):
        name = inp[inp.find(" ") + 1:]
        enemies = [e for e in enemies_in_range if e.name == name]
        if enemies:
            await battle(msg, state, hero, enemies_in_range, enemies[0])
    await state.update_data(enemies_in_range=enemies_in_range)


@form_router.message(GameStates.die)
async def die(msg, state) -> None:
    """Handling the death state of the game's protagonist

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.die)
    inp: Optional[str] = msg.text
    text = c.Phrases.DEFEAT.value
    keys = [b.QUICK_LOAD_BTN, b.LOAD_BTN, b.EXIT_BTN]
    if inp in [b.QUICK_LOAD, b.LOAD]:
        await state.set_state(GameStates.save_menu)
        await save_menu_handle(msg, state)
    elif inp == b.EXIT:
        text = "Игра начинается заново"
        keys = []
        await start(msg, state)
    else:
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(
    GameStates.run, F.text.in_([b.BTNS_MEAN["whereami"], "Осмотреться"])
)
async def show_whereami(msg: Message, state: FSMContext):
    """Show message that contains name, hp, position

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    if msg.text == b.BTNS_MEAN["whereami"]:
        hero = DATA["hero"]
        text = hero.get_person_info()
        pos: c.Direction = hero.whereami()
        text += f" находится на [{pos.x}, {pos.y}]\n"
        await msg.answer(text)
        await msg.answer(await show_map(msg, state))
        text = "Куда направлемся?"
        await msg.answer(text, reply_markup=await create_keyboard(b.DIR_BTNS))
        await state.set_state(GameStates.choose_location.state)
    else:
        await msg.answer(await show_map(msg, state))
        await choose_action(msg, state)


async def show_map(msg: Message, state: FSMContext) -> str:
    """Shows game map - current location by protagonist.location_id

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    hero: c.Protagonist = DATA["hero"]
    lid: int = hero.location_id
    field: List[List[str]] = copy.deepcopy(DATA["fields"][lid - 1])
    y_max: int = len(field) - 1
    x_max = len(field[y_max])
    NPCs = DATA["npcs"] + DATA["enemies"]

    map_quest_handle(hero, NPCs, field, lid, y_max)

    for npc in NPCs:
        if npc.location_id == lid and npc.hp > 0:
            map_npc_handle(npc, field, y_max, x_max)

    pos: c.Direction = hero.whereami()
    if y_max - pos.y > -1 and pos.y > -1 and pos.x > -1 and pos.x < x_max:
        field[y_max - pos.y][pos.x] = hero.appearance

    text: str = ""
    for row in field:
        text += "".join(row)
        text += "\n"

    return text


def map_quest_handle(
    hero: c.Protagonist,
    NPCs: List[c.NPC],
    field: List[List[str]],
    lid: int,
    y_max: int,
) -> None:
    """Handling display quest items for "trace" quests

    Parameters
    ----------
    hero : c.Protagonist
        The protagonist of game
    NPCs: List[c.NPC]
        List of NPCs that can give quests
    field : List[str]
        The current location where the action take place
    lid : int
        The location ID
    y_max : int
        The current location length
    """

    for quest in [
        q
        for q in hero.questbook
        if not q.is_done
        and q.kind == c.QuestKind.TRACE
        and q.location_id == lid
    ]:
        quest_trace_handle(NPCs, field, quest, y_max)


def quest_trace_handle(
    NPCs: List[c.NPC], field: List[List[str]], quest: c.Quest, y_max: int
) -> None:
    """Makes trace path or uses ready-made path

    Parameters
    ----------
    NPCs: List[c.NPC]
        List of NPCs that can give quests
    field : List[str]
        The current location where the action take place
    quest : c.Quest
        The quest with the kind "trace"
    y_max : int
        The current location length
    """

    if quest.id not in DATA["traces"]:
        start_pos, end_pos = None, None
        for npc in NPCs:
            if npc.id == quest.giving_npc_id:
                start_pos = copy.deepcopy(npc.whereami())
            elif npc.id == quest.receiving_npc_id:
                end_pos = npc.whereami()
            if start_pos and end_pos:
                break
        if start_pos and end_pos:
            make_trace(field, start_pos, end_pos, quest, y_max)
    else:
        for pos in DATA["traces"][quest.id]:
            field[y_max - pos.y][pos.x] = quest.item


def make_trace(
    field: List[List[str]],
    start: c.Direction,
    end: c.Direction,
    quest: c.Quest,
    y_max: int,
) -> None:
    """Makes a trace path

    Parameters
    ----------
    field : List[List[str]]
        The current location where the action take place
    start: c.Direction
        Start trace position
    end: c.Direction
        End trace position
    quest : c.Quest
        The quest with the kind "trace"
    y_max : int
        The current location length
    """

    DATA["traces"][quest.id] = []
    is_done: bool = False
    while not is_done:
        if start.x == end.x and start.y == end.y:
            is_done = True
        elif start.x != end.x and start.y != end.y:
            is_x = r.randint(0, 1)
            if is_x:
                start.x += 1 if end.x > start.x else -1
            else:
                start.y += 1 if end.y > start.y else -1
        elif start.x != end.x:
            start.x += 1 if end.x > start.x else -1
        elif start.y != end.y:
            start.y += 1 if end.y > start.y else -1
        if field[y_max - start.y][start.x] in DATA["map_free"] and not (
            start.x == end.x and start.y == end.y
        ):
            new_pos = copy.deepcopy(start)
            DATA["traces"][quest.id].append(new_pos)
            field[y_max - start.y][start.x] = quest.item


def map_npc_handle(
    npc: Union[c.NPC, c.Enemy],
    field: List[List[str]],
    y_max: int,
    x_max: int
) -> None:
    """NPC placement by location

    Parameters
    ----------
    npc : NPC
        NPC to be placed
    field : List[List[str]]
        The current location where the action take place
    y_max : int
        The current location length
    x_max : int
        The current location width
    """

    pos: c.Direction = npc.whereami()
    check: c.Position = c.Position.CORRECT
    map_free = DATA["map_free"] + DATA["init"]["appearances"]
    if y_max - pos.y > -1 and pos.y > -1 and pos.x > -1 and pos.x < x_max:
        if field[y_max - pos.y][pos.x] not in map_free:
            check = c.Position.OBSTACLE
        else:
            field[y_max - pos.y][pos.x] = npc.appearance
    else:
        check = c.Position.OUT_FIELD

    if check != c.Position.CORRECT:
        text: str = f"NPC {npc.name} position incorrect: [{pos.x} {pos.y}]"
        if check == c.Position.OBSTACLE:
            text += f" is obstacle {field[y_max - pos.y][pos.x]}"
        elif check == c.Position.OUT_FIELD:
            text += " is out of field"
        logging.warning(text)


@form_router.message(GameStates.choose_location)
async def choose_location(msg: Message, state: FSMContext):
    """Show message for wich location you can going

    Parametrs
    ---------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    hero: c.Protagonist = DATA["hero"]
    text = msg.text
    out: str = ""
    keys: List[Any] = []
    new_state: Optional[str] = GameStates.choose_sub_loc.state
    if text == b.DIR_BTNS_MEAN["North"]:
        await state.update_data(dir="North")
        out = "В какую локацию севера?"
        keys = split_buttons(b.NORTH_BTNS)
    elif text == b.DIR_BTNS_MEAN["South"]:
        await state.update_data(dir="South")
        out = "В какую локацию юга?"
        keys = split_buttons(b.SOUTH_BTNS)
    elif text == b.DIR_BTNS_MEAN["East"]:
        await state.update_data(dir="East")
        out = "В какую локацию востока?"
        keys = split_buttons(b.EAST_BTNS)
    elif text == b.DIR_BTNS_MEAN["West"]:
        await state.update_data(dir="West")
        out = "В какую локацию запада?"
        keys = split_buttons(b.WEST_BTNS)
    elif text == b.DIR_BTNS_MEAN["Begining"]:
        hero.location_id = 1
        hero.set_pos(0, 0)
        set_npc_new_loc(hero, hero.location_id)
        await msg.answer(await show_map(msg, state))
        out = "Вы вернулись в начало"
    elif text == b.BACK:
        out = "Куда направляемся?"
        keys = b.DIR_BTNS
        new_state = GameStates.choose_location.state
    else:
        out = "Выберите направление."
        new_state = await state.get_state()
    await msg.answer(out, reply_markup=await create_keyboard(keys))
    await state.set_state(new_state)
    await choose_action(msg, state) if text == b.DIR_BTNS_MEAN[
        "Begining"
    ] else None


@form_router.message(GameStates.choose_sub_loc)
async def choose_sub_loc(msg: Message, state: FSMContext):
    """Show message for which subloc you can going

    Parametrs
    ---------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    hero: c.Protagonist = DATA["hero"]
    inp: Optional[str] = msg.text
    data = await state.get_data()
    dir = data.get("dir")

    loc_buttons_mean = {}
    if dir == "North":
        loc_buttons_mean = b.NORTH_BTNS_MEAN
    elif dir == "South":
        loc_buttons_mean = b.SOUTH_BTNS_MEAN
    elif dir == "East":
        loc_buttons_mean = b.EAST_BTNS_MEAN
    elif dir == "West":
        loc_buttons_mean = b.WEST_BTNS_MEAN

    if inp and inp in loc_buttons_mean:
        lid: Optional[int] = b.ALL_DIRS_MEAN.get(inp, None)
        if lid:
            hero.location_id = lid
        else:
            raise ValueError("Неизвестная локация")
        hero.set_pos(0, 0)
        set_npc_new_loc(hero, lid)
        out: str = f"Вы попали в {inp}"
        await msg.answer(out)
        await msg.answer(await show_map(msg, state))
        await choose_action(msg, state)
    else:
        await msg.answer("Выберите локацию")


def set_npc_new_loc(hero: c.Protagonist, lid: int) -> None:
    """Unique NPC placement by location

    Parameters
    ----------
    hero : c.Protagonist
        The protagonist of game
    lid : int
        The location ID
    """

    special_condition: bool = False
    for npc in DATA["union"]:
        npc.location_id = lid
        npc.set_pos(0, 0)
        special_condition = True
    for npc in DATA["pursuit"]:
        npc.location_id = lid
        npc.set_pos(0, 0)
        special_condition = True
    if special_condition:
        hero.set_pos(1, 1)


@form_router.message(GameStates.run, F.text == b.BTNS_MEAN["inventory"])
async def show_inventory(msg: Message, state: FSMContext):
    """Print the protagonists inventory

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.inventory)
    hero = DATA["hero"]
    text: str = "<u>" + hero.get_person_info() + "</u>\n"

    text += "\nТекущее оружие\n"
    wpn = hero.weapon
    text += f"{wpn.name} {wpn.dmg_min}-{wpn.dmg_max} 🗡, {wpn.range} 🎯\n"

    text += "\nТекущая одежда\n"
    armor = hero.armor
    text += f"{armor.name} {armor.buff} 🛡\n"

    text += "\n<u>В инвентаре:</u>\n"
    weaponry: List[Tuple[c.Weapon, int]] = []
    armory: List[Tuple[c.Item, int]] = []
    for item, quantity in hero.inventory.items():
        if isinstance(item, c.Item) and item != DATA["std_armor"]:
            if item.buff_parameter == c.ItemBuff.DEFENSE:
                armory.append((item, quantity))
            else:
                text += f"{item.name}: {quantity} шт.\n"
        elif isinstance(item, c.Weapon) and item != DATA["std_weapon"]:
            weaponry.append((item, quantity))

    for w, q in weaponry:
        text += (
            f"{w.name}: урон {w.dmg_min}-{w.dmg_max} 🗡, "
            f"дальность {w.range} 🎯, {q} шт.\n"
        )
    for a, q in armory:
        text += f"{a.name}: защита {a.buff}, {q} шт.\n"
    keys = [
        b.SHOW_QUESTS_BTN,
        b.USE_BTN,
        b.CHOOSE_WEAPON_BTN,
        b.CHOOSE_ARMOR_BTN,
        b.THROW_OUT_BTN,
    ]
    all_npcs = DATA["npcs"] + DATA["enemies"]
    await loot_in_range(state, hero, all_npcs, keys)
    keys = split_buttons(keys)
    await msg.answer(
        text, parse_mode="HTML", reply_markup=await create_keyboard(keys)
    )


async def loot_in_range(
    state: FSMContext,
    hero: c.Protagonist,
    npcs: List[Any],
    keys: List[KeyboardButton],
    battle_mode=False,
) -> None:
    """Adds names of NPCs that have died to loot buttons

    state : FSMContext
        FSM state context
    hero : c.Protagonist
        The protagonist of game
    npcs : List[Union[c.NPC, c.Enemy]]
        The NPCs whom could be looted
    keys: List[KeyboardButton]
        Telegram keyboard keys
    battle_mode: bool, optional
        if loot in battle
    """

    loot_range: int = 2

    if battle_mode:
        defeated_npcs: List[Union[c.NPC, c.Enemy]] = []
        st_data: Dict[str, Any] = await state.get_data()
        npcs_lootable: List[Union[c.NPC, c.Enemy]] = st_data["npcs_lootable"]
    else:
        npcs_lootable = []

    for npc in npcs:
        if npc.hp <= 0:
            defeated_npcs.append(npc) if battle_mode else None
            if npc.inventory and hero.is_in_range(npc, loot_range):
                keys.append(KeyboardButton(text=f"{b.LOOT} у {npc.name}"))
                npcs_lootable.append(npc) if npc not in npcs_lootable else None

    await state.update_data(npcs_lootable=npcs_lootable)

    if battle_mode:
        for npc in defeated_npcs:
            npcs.remove(npc)


@form_router.message(GameStates.inventory)
async def inventory_handle(msg: Message, state: FSMContext):
    """Inventory menu

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    text: str = "Выберите предмет:"
    keys = []
    hero = DATA["hero"]
    if inp == b.CHOOSE_WEAPON:
        await state.set_state(GameStates.choose_weapon)
        for w in hero.inventory:
            if isinstance(w, c.Weapon):
                keys.append(KeyboardButton(text=w.name))
        text = "Выберите оружие:"
    elif inp == b.CHOOSE_ARMOR:
        await state.set_state(GameStates.choose_armor)
        for a in hero.inventory:
            if isinstance(a, c.Item) and a.is_armor:
                keys.append(KeyboardButton(text=a.name))
        text = "Выберите одежду:"
    elif inp == b.THROW_OUT:
        await state.set_state(GameStates.throw)
        for item in hero.inventory:
            if item not in [
                DATA["std_armor"],
                DATA["std_weapon"],
                hero.weapon,
                hero.armor,
            ]:
                keys.append(KeyboardButton(text=item.name))
    elif inp == b.USE:
        await state.set_state(GameStates.use)
        for item in hero.inventory:
            if type(item) is c.Item and item.is_usable:
                keys.append(KeyboardButton(text=item.name))
    elif inp == b.SHOW_QUESTS:
        await state.set_state(GameStates.show_quests)
        text = "Выберите квест:"
        keys = [
            KeyboardButton(text=q.brief)
            for q in hero.questbook
            if not q.is_done
        ]
    elif inp and inp.startswith(b.LOOT):
        st_data: Dict[str, Any] = await state.get_data()
        npcs_lootable = st_data.get("npcs_lootable", [])
        name: str = inp[inp.find("у ") + 2:]
        text = hero.loot(name, DATA, npcs_lootable)
    else:
        text = ""
        await show_inventory(msg, state)
    keys = split_buttons(keys)
    if text:
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.show_quests)
async def show_quests(msg: Message, state: FSMContext) -> None:
    """Shows uncompleted tasks

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    text: str = ""
    keys: List[KeyboardButton] = []
    hero = DATA["hero"]
    if inp == "Выбрать другой квест 🔄":
        text = "Выберите квест:"
        keys = split_buttons(
            [
                KeyboardButton(text=q.brief)
                for q in hero.questbook
                if not q.is_done
            ]
        )
    else:
        quests = [q.description for q in hero.questbook if q.brief == inp]
        if quests:
            text = quests[0]
        keys = split_buttons([KeyboardButton(text="Выбрать другой квест 🔄")])
    if text:
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.use)
async def use(msg: Message, state: FSMContext) -> None:
    """Use the item to get its boost

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    item_name: Optional[str] = msg.text
    hero = DATA["hero"]
    items = hero.inventory
    text: str = ""
    if item_name not in [i.name for i in items]:
        text = "Такого предмета нет"
    else:
        text = "<u>Выбрано</u>"
        text += "\n" + item_name + "\n"
        found_items = [i for i in items if i.name == item_name and i.is_usable]
        if found_items:
            text += use_buff_item(found_items[0], hero)
        else:
            text += "Этот предмет нельзя использовать"

    await msg.answer(
        text, parse_mode="HTML", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(GameStates.inventory)
    await inventory_handle(msg, state)


def use_buff_item(item: c.Item, hero: c.Protagonist) -> str:
    """Handle items that enhance the player

    Parameters
    ----------
    item : c.Item
        The buff item
    hero : c.Protagonist
        The game's protagonist

    Returns
    -------
    str
        The information message about using item
    """

    text: str = ""
    is_used: bool = False
    items: List[str] = [i.name for i in DATA["items_duration"]]
    if item.buff_parameter == c.ItemBuff.HP:
        text += "\n" + hero.heal(item.buff)
        is_used = True
    elif item.buff_parameter == c.ItemBuff.DAMAGE:
        if item not in items:
            hero.weapon.dmg_min += item.buff
            hero.weapon.dmg_max += item.buff
            text += f"\nУсилен урон от оружия на {item.buff}"
            is_used = True
    elif item.buff_parameter == c.ItemBuff.DEFENSE:
        if item not in items:
            hero.armor.buff += item.buff
            text += f"\nУсилена броня на {item.buff}"
            is_used = True
    if is_used:
        DATA["items_duration"].append(
            copy.deepcopy(item)) if item.duration else None
        hero.throw(item)
    return text


@form_router.message(GameStates.choose_weapon)
async def choose_weapon(msg: Message, state: FSMContext) -> None:
    """Change the weapon of protagonist

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    in_list: bool = False
    weapon: c.Weapon
    hero = DATA["hero"]
    for w in hero.inventory:
        if isinstance(w, c.Weapon) and inp and w.name in inp:
            in_list = True
            weapon = w
            break
    if in_list:
        hero.weapon = weapon
    await choose_action(msg, state)


@form_router.message(GameStates.choose_armor)
async def choose_armor(msg: Message, state: FSMContext) -> None:
    """Change the armor of protagonist

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    in_list: bool = False
    armor: c.Item
    hero = DATA["hero"]
    for a in hero.inventory:
        if isinstance(a, c.Item):
            if (
                a.buff_parameter == c.ItemBuff.DEFENSE
                and inp
                and a.name in inp
            ):
                in_list = True
                armor = a
                break
    if in_list:
        hero.armor = armor
    await choose_action(msg, state)


@form_router.message(GameStates.throw)
async def throw_out(msg: Message, state: FSMContext):
    """Choose item and throw it

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    in_list: bool = False
    item_out: str
    for item, quantity in DATA["hero"].inventory.items():
        if item.name == msg.text:
            in_list = True
            item_out = item
            break
    if in_list:
        await state.update_data(item_out=item_out)
        await state.set_state(GameStates.reduce_item)
        text: str = "Введите количество"
        keys = [b.ALL_BTN, b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))
    else:
        text = "Нет такого предмета"
        keys = [b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.reduce_item)
async def reduce_item(msg: Message, state: FSMContext):
    """Reduce item quantity

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    st_data: Dict[str, Any] = await state.get_data()
    item = st_data["item_out"]
    reduce: int = 0
    hero = DATA["hero"]
    inp: Optional[str] = msg.text
    if msg.text == b.ALL:
        reduce = hero.inventory[item]
    elif inp:
        reduce = int(inp)
    hero.throw(item, reduce)

    await state.set_state(GameStates.run)
    await show_inventory(msg, state)


@form_router.message(GameStates.run, F.text == b.BTNS_MEAN["talk"])
async def talk(msg: Message, state: FSMContext):
    """Talk with npc

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.talk)
    npcs: List[c.NPC] = DATA["npcs"] + DATA["enemies"]
    hero: c.Protagonist = DATA["hero"]
    talk_range: int = 2
    npcs_in_range: List[c.NPC] = []
    for npc in npcs:
        if npc.hp > 0 and hero.is_in_range(npc, talk_range):
            npcs_in_range.append(npc)
    text: str = "С кем поговорить? 🗣"
    keys = [KeyboardButton(text=n.name) for n in npcs_in_range]
    keys = split_buttons(keys)
    await state.update_data(talk=npcs_in_range)
    await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.talk)
async def talk_menu(msg: Message, state: FSMContext):
    """Talk menu handle

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    st_data: Dict[str, Any] = await state.get_data()
    npcs_in_range: List[c.NPC] = st_data["talk"]
    npc: Optional[c.NPC] = None
    for n in npcs_in_range:
        if inp and inp in n.name:
            npc = n
            break
    if npc is not None:
        await state.update_data(npc=npc)
        await state.set_state(GameStates.talk_with)
        text: str = "Выберите действие:"
        keys = [b.TALK_WITH_BTN, b.TRADE_BTN, b.INSPECT_BTN]
        union_farewell(npc, keys)
        keys = split_buttons(keys)
        await msg.answer(text, reply_markup=await create_keyboard(keys))


def union_farewell(npc: c.NPC, keys: List[KeyboardButton]) -> None:
    """Append break up the squad keys

    Parameters
    ----------
    npc: c.NPC
        The NPC in union
    keys : List[KeyboardButton]
        The talk menu keys
    """

    if npc in DATA["union"]:
        keys.append(
            KeyboardButton(text=f"{c.Phrases.BREAK_UNION.value} {npc.name}")
        )


@form_router.message(GameStates.talk_with)
async def talk_to_npc(msg: Message, state: FSMContext):
    """Talk or trade with choosen npc

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    st_data: Dict[str, Any] = await state.get_data()
    npc = st_data["npc"]
    inp: Optional[str] = msg.text
    hero = DATA["hero"]
    if inp == b.TALK_WITH:
        await state.set_state(GameStates.dialogue)
        await dialogue(msg, state)
    elif inp == b.TRADE:
        if npc not in DATA["enemies"]:
            await state.set_state(GameStates.trade)
            await trade(msg, state)
        else:
            text: str = "С ним не получится торговать"
            keys = [b.BACK_BTN]
            await msg.answer(text, keys=await create_keyboard(keys))
    elif inp == b.INSPECT:
        cls_name: str = "".join(
            [name for name, v in c.PLAYABLE_CLS.items() if v == npc.class_id]
        )
        text = (
            f"Перед вами {cls_name} {npc.name}\n"
            f"В руках держит {npc.weapon.name}\nВыглядит "
        )
        if npc.hp <= hero.hp * 1.2 and npc.hp >= hero.hp * 0.8:
            text += "также как и вы"
        elif npc.hp > hero.hp:
            text += "сильнее вас"
        else:
            text += "слабее вас"
        keys = [b.BACK_BTN]
        await msg.answer(text, keys=await create_keyboard(keys))
    elif inp and inp.startswith(c.Phrases.BREAK_UNION.value):
        text = f"{npc.name} не в союзе"
        keys = [b.BACK_BTN]
        if npc in DATA["union"]:
            DATA["union"].remove(npc)
            text = f"{npc.name} покинул вас"
        await msg.answer(text, keys=await create_keyboard(keys))


@form_router.message(GameStates.dialogue)
async def dialogue(msg: Message, state: FSMContext) -> None:
    """Dialogue with NPC

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = (
        msg.text if msg.text != b.TALK_WITH else c.Phrases.INIT.value
    )
    st_data: Dict[str, Any] = await state.get_data()
    npc = st_data["npc"]
    hero = DATA["hero"]
    answer = hero.talk_to(npc, inp, DATA)
    text: str = answer["text"]
    keys = [KeyboardButton(text=r) for r in answer["response"]]
    ends = [
        c.Phrases.END_CIV.value,
        c.Phrases.END_CON.value,
        c.Phrases.END_COR.value,
    ]
    angry_ends = [c.Phrases.ANGRY_END_CON.value, c.Phrases.ANGRY_END_COR.value]
    quest_ends = [
        c.Phrases.GRATITUDE_CIV.value,
        c.Phrases.GRATITUDE_CON.value,
        c.Phrases.GRATITUDE_COR.value,
        c.Phrases.UPSET_CIV.value,
        c.Phrases.UPSET_CON.value,
        c.Phrases.UPSET_COR.value,
    ]
    is_end: str = ""
    for end in ends + angry_ends + quest_ends + [c.Phrases.WIN_REACT.value]:
        if end in text:
            if text in angry_ends:
                is_end = "angry"
            else:
                is_end = "ordinary"
            break
    await msg.answer(
        text, parse_mode="HTML", reply_markup=await create_keyboard(keys)
    )
    if is_end == "ordinary":
        text = hero.check_quests(npc, DATA)
        await msg.answer(text, parse_mode="HTML") if text else None
        await choose_action(msg, state)
    elif is_end == "angry":
        await state.set_state(GameStates.attack)
        await get_enemies_in_range(state)
        await state.update_data(npcs_lootable=[])
        await battle(msg, state, hero, [npc], npc)
    elif inp and inp.startswith(c.Phrases.LETS_PLAY.value):
        if [
            q
            for q in hero.questbook
            if q.kind == c.QuestKind.GO and not q.is_done
        ]:
            await state.set_state(GameStates.start_game)
            await play_go(msg, state)


@form_router.message(GameStates.trade, F.text == b.DONE)
async def trade_done_condition(msg: Message, state: FSMContext) -> None:
    """Trade state done condition

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.trade_list)
    await trade_done(msg, state)


@form_router.message(GameStates.trade)
async def trade(msg: Message, state: FSMContext) -> None:
    """Main trade menu

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    st_data: Dict[str, Any] = await state.get_data()
    if inp == b.BUY or inp == b.SELL:
        await state.set_state(GameStates.trade_list)
        if inp == b.BUY:
            await state.update_data(trade="buy")
            st_data["buy"] = st_data.get("buy", {"sum": 0})
            await state.update_data(buy=st_data["buy"])
        elif inp == b.SELL:
            await state.update_data(trade="sell")
            st_data["sell"] = st_data.get("sell", {"sum": 0})
            await state.update_data(sell=st_data["sell"])
        await trade_list(msg, state)
    else:
        text: str = ""
        hor_width: int = 30
        text += print_trade_status(st_data, "buy", hor_width)
        text += "".join([" " if i % 2 == 1 else "_" for i in range(hor_width)])
        text += "\n"
        text += print_trade_status(st_data, "sell", hor_width)
        keys = [b.BUY_BTN, b.SELL_BTN, b.DONE_BTN, b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


def print_trade_status(
    st_data: Dict[str, Any], trade_type: str, hor_width: int
) -> str:
    """Shows trade status

    Parameters
    ----------
    st_data: Dict[str, Any]
        The state dictionary
    trade_type: str
        Buy or sell
    hor_width: int
        The length of divider

    Returns
    -------
    str
        Trade status
    """

    text: str = ""
    if trade_type == "buy":
        text += "Выбранные товары продавца:\n"
    elif trade_type == "sell":
        text += "Выбранные товары персонажа:\n"
    text += hor_width * "_" + "\n"
    for item, quantity in st_data.get(trade_type, {}).items():
        if item != "sum":
            text += f"{item.name}: {quantity} шт.\n"
    text += "Общая стоимость - "
    cost: int = st_data.get(trade_type, {}).get("sum", 0)
    text += str(cost)
    text += cost_naming(cost) + "\n"
    return text


def cost_naming(cost: int) -> str:
    """Gives the correct declination for the number of coins

    Parameters
    ----------
    cost: int
        The coins quantity

    Returns
    -------
    str
        The correct declension
    """

    declension: str = " пиастр"
    remainder = cost % 10
    if remainder == 1 and cost != 11:
        declension += "а"
    elif remainder in [2, 3, 4] and cost not in [12, 13, 14]:
        declension += "ы"
    return declension


@form_router.message(GameStates.trade_list, F.text.in_([b.BUY, b.SELL]))
async def trade_list(msg: Message, state: FSMContext) -> None:
    """Shows the list of tradable items

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    st_data: Dict[str, Any] = await state.get_data()
    npc = st_data["npc"]
    trade_type = st_data["trade"]
    person = npc if trade_type == "buy" else DATA["hero"]
    text: str = ""
    if trade_type == "buy":
        text = "Выберите товары на покупку:\n"
    elif trade_type == "sell":
        text = "Выберите товары на продажу:\n"

    text += len(text) * "_" + "\n"
    keys = []
    trade_dict = st_data.get(trade_type, {"sum": 0})
    for item, quantity in person.inventory.items():
        if item.is_tradable:
            if (
                item not in [person.weapon, person.armor]
                or person.inventory[item] > 1
            ):
                quantity -= trade_dict.get(item, 0)
                if quantity:
                    text += trade_list_show(item, quantity, keys)
    keys = split_buttons(keys + [b.DONE_BTN])
    await msg.answer(text, reply_markup=await create_keyboard(keys))


def trade_list_show(
        item: c.Item,
        quantity: int,
        keys: List[KeyboardButton]) -> str:
    """Shows trade list status

    Parameters
    ----------
    item : c.Item
        The tradable item
    quantity : int
        The quantity of item
    keys : List[KeyboardButton]
        The Telegram menu keys

    Returns
    -------
    str
        The informational message about item trade
    """

    text: str = ""
    if item.name == "Пиастра":
        text += str(quantity)
        text += cost_naming(quantity)
    else:
        if item.cost:
            text += f"{item.name}: {item.cost}"
            text += cost_naming(item.cost)
        else:
            logging.info(f"{item.name} did not find")
        if quantity > 1:
            text += f" (Осталось {quantity} шт.)"
    text += "\n"
    keys.append(KeyboardButton(text=item.name))
    return text


@form_router.message(GameStates.trade_list, F.text == b.DONE)
async def trade_done(msg: Message, state: FSMContext) -> None:
    """Completes the deal if successful

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    st_data: Dict[str, Any] = await state.get_data()
    npc = st_data["npc"]
    buy_dict = st_data.get("buy", {})
    sell_dict = st_data.get("sell", {})
    if sell_dict.get("sum", 0) < buy_dict.get("sum", 0) or not len(sell_dict):
        text: str = "Так не пойдёт! Плати еще"
        await msg.answer(text)
        await state.set_state(GameStates.trade)
        await trade(msg, state)
    else:
        hero = DATA["hero"]
        for item, quantity in st_data.get("buy", {}).items():
            if isinstance(item, c.Item) or isinstance(item, c.Weapon):
                npc.give(hero, item, quantity)
        for item, quantity in st_data["sell"].items():
            if isinstance(item, c.Item) or isinstance(item, c.Weapon):
                hero.give(npc, item, quantity)
        await clean_list_trade(state)
        text = "По рукам!"
        await msg.answer(text)
        await choose_action(msg, state)


async def clean_list_trade(state: FSMContext) -> None:
    """Cleans buy, sell dictionaries

    Parameters
    ----------
    state : FSMContext
        FSM state context
    """

    await state.update_data(buy={"sum": 0})
    await state.update_data(sell={"sum": 0})


@form_router.message(GameStates.trade_list)
async def trade_quantity(msg: Message, state: FSMContext) -> None:
    """Invites to input the choosen item quantity

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    st_data: Dict[str, Any] = await state.get_data()
    trade_type: str = st_data["trade"]
    person = st_data["npc"] if trade_type == "buy" else DATA["hero"]
    inventory: Dict[Union[c.Item, c.Weapon], int] = person.inventory

    if msg.text not in [item.name for item, quantity in inventory.items()]:
        text: str = "Такого предмета нет"
        await msg.answer(text, reply_markup=ReplyKeyboardRemove())
        await trade_list(msg, state)
    else:
        await state.set_state(GameStates.trade_item)
        item_name: Optional[str] = msg.text
        item_found: Union[c.Item, c.Weapon]
        available_quantity: int = 0
        for item, quantity in inventory.items():
            if item.name == item_name and item.is_tradable:
                item_found = item
                available_quantity = quantity
                await state.update_data(item=item_found)
                available_quantity -= st_data.get(trade_type, {}).get(
                    item_found, 0
                )
                break

        text = "Введите количество"
        keys: List[KeyboardButton] = []
        if available_quantity:
            i: int = 1
            add: int = available_quantity // 5
            add = 1 if add == 0 else add
            while i <= available_quantity:
                keys.append(KeyboardButton(text=str(i)))
                i += add
            last_key = KeyboardButton(text=str(available_quantity))
            if last_key not in keys:
                keys.append(last_key)

            i = -1
            add = -available_quantity // 5
            while i > -available_quantity:
                keys.append(KeyboardButton(text=str(i)))
                i += add
            last_key = KeyboardButton(text=str(-available_quantity))
            if last_key not in keys:
                keys.append(last_key)

            keys = split_buttons(keys)
        else:
            keys = [b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.trade_item)
async def trade_item(msg: Message, state: FSMContext) -> None:
    """Changes item quantity in trade dictionary

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    quantity: int = int(msg.text) if msg.text else 0
    st_data: Dict[str, Any] = await state.get_data()
    item: Optional[c.Item] = st_data.get("item", None)
    trade_type: Optional[str] = st_data.get("trade", None)

    if item and trade_type:
        trade_dict = st_data.get(trade_type, {})
        trade_dict.setdefault(item, 0)
        if quantity < 0:
            available_quantity = trade_dict[item]
            available_quantity += quantity
            quantity -= available_quantity if available_quantity < 0 else 0
        else:
            person = st_data["npc"] if trade_type == "buy" else DATA["hero"]
            inventory: Dict[Union[c.Item, c.Weapon], int] = person.inventory

            available_quantity = [
                q for i, q in inventory.items() if i == item
            ][0]
            available_quantity -= trade_dict.get(item, 0)
            available_quantity -= quantity
            quantity += available_quantity if available_quantity < 0 else 0

        trade_dict[item] += quantity
        trade_dict["sum"] += item.cost * quantity

        await state.set_state(GameStates.trade)
        await trade(msg, state)


@form_router.message(GameStates.start_game)
async def play_go(msg: Message, state: FSMContext) -> None:
    """Initializing a Go game

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.game_go)
    st_data: Dict[str, Any] = await state.get_data()
    npc = st_data["npc"]
    text_width: int = 32
    text: str = "Нужно собрать 5 фигур в ряд\n"
    await msg.answer(text)
    text_part: str = "Первым ходит"
    rows: int = 10
    cols: int = 8
    space: str = " "
    field: List[List[str]] = [
        [space for _ in range(cols)] for _ in range(rows)
    ]
    move: int = 0
    chance: int = r.randint(0, 1)
    if chance:
        text_part += "е вы"
        player_sym = "X"
        npc_sym = "O"
        move += 1
    else:
        text_part += f" {npc.name}"
        npc_sym = "X"
        player_sym = "O"
        row: int = r.randint(0, 9)
        col: int = r.randint(0, 7)
        field[row][col] = "X"
    keys: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=c, callback_data=f"{y} {x}")
            for x, c in enumerate(row)
        ]
        for y, row in enumerate(field)
    ]
    text = text_part + space * (text_width - len(text_part))
    game_go: Dict[str, Any] = {
        "field": field,
        "rows": rows,
        "cols": cols,
        "space": space,
        "npc": npc_sym,
        "player": player_sym,
        "turn": chance,
        "move": move,
        "npc_name": npc.name,
    }
    await state.update_data(game_go=game_go)
    await msg.answer(
        text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keys)
    )


@form_router.callback_query(GameStates.game_go)
async def game_go_round(callback: CallbackQuery, state: FSMContext) -> None:
    """Processing the progress of a game in go

    Parameters
    ----------
    callback : CallbackQuery
        Data obtained from InlineKeyboardButton
    state : FSMContext
        FSM state context
    """

    await callback.answer()
    inp: Optional[str] = callback.data
    st_data: Dict[str, Any] = await state.get_data()
    if inp == "Try again":
        await state.set_state(GameStates.start_game)
        await play_go(callback.message, state)
    elif inp and inp.startswith("Game Over"):
        await game_go_game_over(
            inp, state, callback, DATA["hero"], st_data["npc"]
        )
    else:
        game_go: Dict[str, Any] = st_data["game_go"]
        is_turn = False
        if game_go["turn"] == 0:
            is_turn = True
            game_go["turn"] = 1

        row, col = [int(i) for i in inp.split()] if inp else (None, None)
        if (
            isinstance(row, int)
            and isinstance(col, int)
            and game_go["field"][row][col] == game_go["space"]
        ):
            game_go["field"][row][col] = game_go["player"]
            is_turn = True
            game_go["move"] += 1
            while (
                game_go["turn"]
                and not game_go_npc_turn(game_go)
                and any(
                    any([c == game_go["space"] for c in row])
                    for row in game_go["field"]
                )
            ):
                pass

        await state.update_data(game_go=game_go)

        keys, text_prt = await go_turn_handle(state, game_go, is_turn)

        text_width: int = 32
        text: str = text_prt + " " * (text_width - len(text_prt))
        if (
            callback
            and callback.message
            and isinstance(callback.message, Message)
        ):
            await callback.message.edit_text(
                text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keys)
            )


def game_go_npc_turn(game_go: Dict[str, Any]) -> bool:
    """Proccessing the npc turn

    Parameters
    ----------
    game_go : Dict[str, Any]
        Dictionary storing game parameters

    Returns
    -------
    bool
        True if turn occurs
    """

    row: Optional[int] = None
    col: Optional[int] = None
    dangers: Dict[Tuple[int, int], Dict[str, float]] = calc_dangers(game_go)
    player_danger: float = 0
    npc_danger: float = 0
    player_pos: Optional[Tuple[int, int]] = None
    npc_pos: Optional[Tuple[int, int]] = None
    for pos, danger in dangers.items():
        if danger["player"] > player_danger:
            player_danger = danger["player"]
            player_pos = pos
        if danger["npc"] > npc_danger:
            npc_danger = danger["npc"]
            npc_pos = pos

    if player_danger >= npc_danger and player_pos:
        row, col = player_pos
    elif npc_pos:
        row, col = npc_pos
    else:
        row, col = r.randint(0, game_go["rows"] - 1), r.randint(
            0, game_go["cols"] - 1
        )

    is_turn: bool = False
    if (
        isinstance(row, int)
        and isinstance(col, int)
        and game_go["field"][row][col] == game_go["space"]
    ):
        game_go["field"][row][col] = game_go["npc"]
        is_turn = True
    return is_turn


def calc_dangers(
    game_go: Dict[str, Any]
) -> Dict[Tuple[int, int], Dict[str, float]]:
    """Calculating the position for the benefit of making a move

    Parameters
    ----------
    game_go : Dict[str, Any]
        Dictionary storing game parameters

    Returns
    -------
    Dict[Tuple[int, int], Dict[str, float]]
        A dictionary where the keys are the positions of cells and the
        values ​​are the danger values ​​of the cell for the player and NPC.
    """

    dangers: Dict[Tuple[int, int], Dict[str, float]] = {}
    for i in range(game_go["rows"]):
        for j in range(game_go["cols"]):
            if game_go["field"][i][j] == game_go["space"]:
                player = calc_danger_cell(game_go, i, j, game_go["player"])
                npc = calc_danger_cell(game_go, i, j, game_go["npc"])
                dangers[(i, j)] = {"player": player, "npc": npc}
    return dangers


def calc_danger_cell(
    game_go: Dict[str, Any], i: int, j: int, sym: str
) -> float:
    """Calculating the cells benefit value

    Parameters
    ----------
    game_go : Dict[str, Any]
        Dictionary storing game parameters
    i : int
        Rows pointer
    j : int
        Columns pointer
    sym : str
        A symbol belonging to either a player or an NPC

    Returns
    -------
    float
        A danger value for cell
    """

    field: List[List[str]] = game_go["field"]
    danger_lvl: float = 0
    cf_init: float = 1.5
    cf: float = cf_init
    row, col = i, j + 1
    while col < game_go["cols"] and field[row][col] == sym:
        col += 1
        danger_lvl += 1 * cf
        cf += cf_init
    cf = cf_init
    col = j - 1
    while col > -1 and field[row][col] == sym:
        col -= 1
        danger_lvl += 1 * cf
        cf += cf_init
    cf = cf_init
    row, col = i + 1, j
    while row < game_go["rows"] and field[row][col] == sym:
        row += 1
        danger_lvl += 1 * cf
        cf += cf_init
    cf = cf_init
    row, col = i - 1, j
    while row > -1 and field[row][col] == sym:
        row -= 1
        danger_lvl += 1 * cf
        cf += cf_init
    cf = cf_init
    row, col = i + 1, j + 1
    while (
        row < game_go["rows"]
        and col < game_go["cols"]
        and field[row][col] == sym
    ):
        row += 1
        col += 1
        danger_lvl += 1 * cf
        cf += cf_init
    cf = cf_init
    row, col = i - 1, j - 1
    while row > -1 and col > -1 and field[row][col] == sym:
        row -= 1
        col -= 1
        danger_lvl += 1 * cf
        cf += cf_init
    cf = cf_init
    row, col = i + 1, j - 1
    while row < game_go["rows"] and col > -1 and field[row][col] == sym:
        row += 1
        col -= 1
        danger_lvl += 1 * cf
        cf += cf_init
    cf = cf_init
    row, col = i - 1, j + 1
    while row > -1 and col < game_go["cols"] and field[row][col] == sym:
        row -= 1
        col += 1
        danger_lvl += 1 * cf
        cf += cf_init
    return danger_lvl


async def go_turn_handle(
    state: FSMContext, game_go: Dict[str, Any], is_turn: bool
) -> Tuple[List[Any], str]:
    """Go game turn processing

    Parameters
    ----------
    state : FSMContext
        FSM state context
    game_go : Dict[str, Any]
        Dictionary storing game parameters
    is_turn : bool
        If is correct turn

    Returns
    -------
    Tuple[List[Any], str]
        A danger value for cell
    """

    text_prt: str = (
        f"Ваши '{game_go['player']}'. Ход {game_go['move']}"
        if is_turn
        else "Выберите корректное поле"
    )

    keys: List[Any] = []
    is_end: c.EndTypes = check_end_game_go(game_go)
    if is_end != c.EndTypes.NOT_END:
        if is_end == c.EndTypes.HERO_WIN:
            text_prt = c.Phrases.WIN.value
        elif is_end == c.EndTypes.NPC_WIN:
            text_prt = f"{game_go['npc_name']} победил"
        elif is_end == c.EndTypes.DRAW:
            text_prt = "Ничья"
        keys = [
            [
                InlineKeyboardButton(
                    text="Сыграть еще раз", callback_data="Try again"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Завершить игру",
                    callback_data="Game Over " + text_prt,
                )
            ],
        ]
    else:
        keys = [
            [
                InlineKeyboardButton(text=c, callback_data=f"{y} {x}")
                for x, c in enumerate(row)
            ]
            for y, row in enumerate(game_go["field"])
        ]
    return keys, text_prt


def check_end_game_go(game_go: Dict[str, Any]) -> c.EndTypes:
    """Checks the go game end condition

    if 5 identical symbols appear in a row horizontally, vertically
    or diagonally, the game ends

    Parameters
    ----------
    game_go : Dict[str, Any]
        Dictionary storing game parameters

    Returns
    -------
    c.EndTypes
        Go game end status
    """

    is_end: c.EndTypes = c.EndTypes.NOT_END
    sym: str = " "
    field: List[List[str]] = game_go["field"]
    array: List[List[str]] = []
    rows: List[List[str]] = field
    cols: List[Any] = list(zip(*field))
    l_diag: List[List[str]] = []
    r_diag: List[List[str]] = []
    offset: int = 5
    for col in range(game_go["cols"] - offset, -1, -1):
        l_diag.append(
            [
                field[k][col + k]
                for k in range(game_go["cols"] - col)
                if k < game_go["rows"]
            ]
        )
    for row in range(game_go["rows"] - offset, 0, -1):
        l_diag.append(
            [
                field[row + k][k]
                for k in range(game_go["rows"] - row)
                if k < game_go["cols"]
            ]
        )

    for col in range(offset - 1, game_go["cols"]):
        r_diag.append(
            [field[k][col - k] for k in range(col + 1) if k < game_go["rows"]]
        )
    for row in range(game_go["rows"] - offset, 0, -1):
        r_diag.append(
            [
                field[row + k][game_go["cols"] - k - 1]
                for k in range(game_go["rows"] - row)
                if k < game_go["cols"]
            ]
        )

    array.extend(rows)
    array.extend(cols)
    array.extend(l_diag)
    array.extend(r_diag)
    matches: List[str] = []
    is_match: bool = False
    is_fill: bool = True
    for line in array:
        is_match, is_fill, sym = check_line(
            line, game_go["space"], is_match, is_fill, matches
        )
    if is_match and game_go["player"] in matches:
        is_end = c.EndTypes.HERO_WIN
    elif is_match:
        is_end = c.EndTypes.NPC_WIN
    elif is_fill:
        is_end = c.EndTypes.DRAW
    return is_end


def check_line(
    line: List[str],
    space: str,
    is_match: bool,
    is_fill: bool,
    matches: List[str],
) -> Tuple[bool, bool, str]:
    """Checks the line to 5 a row

    Parameters
    ----------
    line: List[str]
        Current line
    space: str
        Space symbol
    is_match: bool
        True if the end-game condition is met
    is_fill: bool
        True if there is no space left on the field
    matches: List[str]
        List of matches symbols, needs to decide winner

    Returns
    -------
    Tuple[bool, bool, str]
        - Is 5 in row.
        - If all the cells of the field have already been visited.
        - Symbol to be checked
    """

    N: int = len(line)
    n: int = 5
    sym: str = line[0]
    cr: int = 1
    for i in range(1, N):
        if line[i] == sym and line[i] != space:
            cr += 1
            if cr == n:
                is_match = True
                matches.append(line[i])
                break
        else:
            sym = line[i]
            cr = 1
        if is_fill and sym == space:
            is_fill = False
    return is_match, is_fill, sym


async def game_go_game_over(
    inp: str,
    state: FSMContext,
    callback: CallbackQuery,
    hero: c.Protagonist,
    npc: c.NPC,
) -> None:
    """Go end game handler

    Parameters
    ----------
    inp : str
        The Game Over message
    state : FSMContext
        FSM state context
    callback : CallbackQuery
        Data of the pressed button
    hero : c.Protagonist
        The protagonist of game
    npc : c.Npc
        NPC that played with
    """

    text: str = ""
    if inp.endswith(c.Phrases.WIN.value):
        for n in npc.questbook:
            for h in hero.questbook:
                if n.kind == c.QuestKind.GO and not n.is_done and n.id == h.id:
                    h.item = "True"
                    text = hero.quest_accept(h, DATA)
                    break
    else:
        text = "Эх, а я думал, что нашёл достойного соперника"
    if callback and callback.message and hasattr(callback.message, "answer"):
        await callback.message.answer(text)

    await state.set_state(GameStates.dialogue)
    await dialogue(callback.message, state)


@form_router.message(GameStates.run, F.text == b.BTNS_MEAN["saves"])
async def save_menu(msg: Message, state: FSMContext) -> None:
    """Save menu

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.save_menu)
    text: str = "Меню сохранения"
    keys = [
        b.QUICK_LOAD_BTN,
        b.LOAD_BTN,
        b.SAVE_BTN,
        b.QUICK_SAVE_BTN,
        b.REMOVE_SAVE_BTN,
    ]
    keys = split_buttons(keys)
    await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.save_menu)
async def save_menu_handle(msg: Message, state: FSMContext) -> None:
    """The save menu categories handle

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text
    session: Session = get_session()
    await state.update_data(session=session)

    save_ids: List[Any] = []
    hero = DATA["hero"]
    if hero is not None:
        persons = session.query(Person).filter_by(id=hero.id).all()
        save_ids = [p.save_id for p in persons] if persons else []
    await state.update_data(save_ids=save_ids)
    if inp == b.QUICK_LOAD or inp == b.QUICK_SAVE:
        if not len(save_ids) and inp == b.QUICK_LOAD:
            text: str = "Нет сохранений!"
            keys = [b.BACK_BTN]
            await msg.answer(text, reply_markup=await create_keyboard(keys))
        elif inp == b.QUICK_LOAD:
            await load(msg, state, max(save_ids), session)
        elif inp == b.QUICK_SAVE:
            t_save: Optional[Save] = (
                session.query(Save)
                .filter(
                    Save.id.in_(save_ids),  # type: ignore
                    Save.description.like(f"%{b.QUICK_SAVE}%"),  # type: ignore
                )
                .first()
            )
            if t_save:
                session.delete(t_save)
                session.commit()
                session.close()
            session = get_session()
            await save(msg, state, session)
    elif inp == b.LOAD:
        await load_choose(msg, state)
    elif inp == b.SAVE:
        text = "Введите описание сохранения:"
        await msg.answer(text, reply_markup=ReplyKeyboardRemove())
        await state.set_state(GameStates.save)
    elif inp == b.REMOVE_SAVE:
        await state.set_state(GameStates.remove_save_menu)
        await remove_save_menu(msg, state)
    session.close()


@form_router.message(GameStates.save)
async def presave(msg: Message, state: FSMContext):
    """Prepare session to save

    Needs to reuse save function by quick save

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    st_data: Dict[str, Any] = await state.get_data()
    session = st_data.get("session", get_session())
    await save(msg, state, session)


async def save(msg: Message, state: FSMContext, session: Session):
    """Saves the game process to tables

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    session: Session
    """

    inp: str = msg.text if msg.text else ""
    save_ids = session.query(Save.id).order_by(Save.id.desc()).first()
    save_id = 1 if save_ids is None else save_ids[0] + 1
    st_data: Dict[str, Any] = await state.get_data()
    hero = DATA["hero"]
    init_time: float = 0
    if save_ids:
        persons_first_save = (
            session.query(Person)
            .filter_by(id=hero.id)
            .order_by(Person.save_id)
            .first()
        )
        if persons_first_save:
            first_save = (
                session.query(Save)
                .filter_by(id=persons_first_save.save_id)
                .first()
            )
            init_time = first_save.time if first_save else 0

    cur_time: float = time.time() - st_data.get("start_time", 0) + init_time

    game_time = (
        f"{cur_time // 3600}:{(cur_time % 3600) // 60}:{round(cur_time % 60)}"
    )
    description = inp + " " + game_time + " | SAVE ID " + str(save_id)

    session.add(Save(id=save_id, description=description, time=cur_time))
    session.commit()
    await save_person(session, save_id, hero)
    for npc in DATA["npcs"] + DATA["enemies"]:
        await save_person(session, save_id, npc)

    session.commit()

    text: str = "Сохранение...\nЗагружайся по uuid ⬇️!\n"
    await msg.answer(text, reply_markup=ReplyKeyboardRemove())
    await msg.answer(text=hero.id)
    await choose_action(msg, state)


async def save_person(
    session: Session,
    save_id: int,
    person: Union[c.Protagonist, c.NPC, c.Enemy],
) -> None:
    """Save Protagonits and NPCs to tables

    Parameters
    ----------
    session: Session
        The PostgreSQL session
    save_id: int
        The current save_id
    person: Union[c.Protagonist, c.NPC, c.Enemy]
        The character class
    """

    t_person = Person()
    setattr(t_person, "save_id", save_id)
    setattr(
        t_person,
        "is_protagonist",
        True if type(person) is c.Protagonist else False,
    )
    for attr, value in person.__dict__.items():
        if attr == "_Protagonist__pos":
            attr = "_Person__pos"
        if hasattr(t_person, attr):
            if attr == "_Person__pos":
                setattr(t_person, attr, [value.x, value.y])
            elif attr == "weapon":
                setattr(t_person, attr, person.weapon.name)
            elif attr == "armor":
                setattr(t_person, attr, person.armor.name)
            else:
                setattr(t_person, attr, value)
    t_person.items = []
    t_person.weapons = []
    t_person.quests = []
    for item, quantity in person.inventory.items():
        if isinstance(item, c.Item):
            t_person.items.append(
                Person_Item(
                    person_id=person.id,
                    save_id=save_id,
                    item_id=item.id,
                    quantity=quantity,
                )
            )
        elif isinstance(item, c.Weapon):
            t_person.weapons.append(
                Person_Weapon(
                    person_id=person.id, save_id=save_id, weapon_id=item.id
                )
            )
    for quest in person.questbook:
        t_person.quests.append(
            Person_Quest(
                person_id=person.id,
                save_id=save_id,
                quest_id=quest.id,
                is_done=quest.is_done,
            )
        )

    if type(person) is c.Protagonist:
        t_person.buff_items = []
        for i in DATA["items_duration"]:
            t_person.buff_items.append(Person_BuffItem(
                person_id=person.id,
                save_id=save_id,
                item_id=i.id,
                duration=i.duration))
    session.add(t_person)
    session.commit()


def parsing_arguments() -> Optional[argparse.Namespace]:
    """Parses command line arguments

    Returns
    -------
    Optional[argparse.Namespace]
        Namespace of parsed arguments
    """

    parser = argparse.ArgumentParser(
        "Write -drop if database has been changed"
    )
    parser.add_argument(
        "-d",
        "--drop",
        action="store_true",
        help="drops corsairs_vs_condottiers database",
    )
    parser.add_argument(
        "-a",
        "--append",
        action="store_true",
        help="append to tables new values",
    )
    parser.add_argument(
        "-c",
        "--correct",
        action="store_true",
        help="corrects table values",
    )
    ns: Optional[argparse.Namespace] = None
    try:
        ns = parser.parse_args()
    except SystemExit as e:
        logging.error("parse_args: %s", e)
    return ns


async def load_choose(msg: Message, state: FSMContext) -> None:
    """Choose load st_data from saves

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    args = DATA.get("args", None)
    is_new: bool = create_db_and_user(args)
    st_data: Dict[str, Any] = await state.get_data()
    session = st_data.get("session", get_session())
    await state.update_data(session=session)
    if is_new or (args and (args.correct or args.append)):
        fd.fill_database(session, args)
    DATA["args"] = None

    ids = session.query(Person.save_id).filter_by(id=DATA["hero"].id).all()
    ids = [id[0] for id in ids]
    saves = session.query(Save.description).filter(Save.id.in_(ids)).all()
    keys = [b.BACK_BTN]
    if len(saves):
        await state.set_state(GameStates.load)
        text: str = "Выберите сохранение: "
        keys = [KeyboardButton(text=s.description) for s in saves]
        keys = split_buttons(keys)
    else:
        text = "Сохранений для этого ID нет"
    session.close()
    await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.load)
async def preload(msg: Message, state: FSMContext):
    """Makes save_id from message, starts session

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    inp: Optional[str] = msg.text

    if inp:
        try:
            save_id: int = int(inp.split()[-1])
            st_data: Dict[str, Any] = await state.get_data()
            session = st_data.get("session", get_session())
            await load(msg, state, save_id, session)
        except ValueError:
            await load_choose(msg, state)


async def load(
    msg: Message, state: FSMContext, save_id: int, session: Session
) -> None:
    """Returns game status from load st_data

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    save_id: int
        The Save table id
    session: Session
        The PostgreSQL session

    Raises
    ------
    ValueError
        If save doesn't exist by given save_id
    """

    save = session.query(Save).filter_by(id=save_id).first()
    if save is None:
        raise ValueError("Не существует сохранения с таким ID")
    global DATA
    DATA = load_all(DATA, save_id=save_id)
    await state.update_data(is_init_load=False)
    await state.update_data(start_time=time.time())
    await msg.answer(await show_map(msg, state))
    text: str = "Загрузка..."
    await msg.answer(text, reply_markup=ReplyKeyboardRemove())
    await choose_action(msg, state)


@form_router.message(GameStates.remove_save_menu)
async def remove_save_menu(msg: Message, state: FSMContext):
    """Menu where you can delete saves

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    st_data: Dict[str, Any] = await state.get_data()
    save_ids = st_data["save_ids"]
    session: Session = st_data["session"]
    if save_ids:
        await state.set_state(GameStates.remove_save)
        text: str = "Выберите сохранение, которое хотите удалить:"
        saves = session.query(Save).filter(Save.id.in_(save_ids)).all()
        keys = [KeyboardButton(text=s.description) for s in saves]
        keys = split_buttons(keys)
    else:
        text = "Сохранений нет"
        await state.set_state(GameStates.remove_save_menu)
        keys = [b.BACK_BTN]
    await msg.answer(text=text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.remove_save)
async def remove_save(msg: Message, state: FSMContext):
    """Remove save handle

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    description: Optional[str] = msg.text
    st_data: Dict[str, Any] = await state.get_data()
    save_ids = st_data["save_ids"]
    saves: List[Save] = []
    session: Session = st_data["session"]
    if save_ids:
        saves = session.query(Save).filter(Save.id.in_(save_ids)).all()
    if description in [s.description for s in saves]:
        save = session.query(Save).filter_by(description=description).first()
        if save:
            save_ids.remove(save.id) if save.id in save_ids else None
            await state.update_data(save_ids=save_ids)
            session.delete(save)
            session.commit()
    await remove_save_menu(msg, state)


@form_router.message(F.text == b.EXIT)
async def exit_game(msg: Message, state: FSMContext):
    """Remove save handle

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    hero = DATA["hero"]
    if hero is None:
        raise ValueError("Персонаж не создан")
    text: str = f"Волны тихо плещутся о берег...\nID {hero.id}"
    await msg.answer(text)


@form_router.message(GameStates.run)
async def choose_action(msg: Message, state: FSMContext):
    """Main game actions

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    await state.set_state(GameStates.run)
    text: str = "Выберите действие:"
    await msg.answer(text, reply_markup=await create_keyboard(b.GAME_BTNS, 3))


async def main(var: str) -> None:
    """Starts the bot's event processing using aiogram.

    Parameters
    ----------
    var: str
        The environment variable
    """

    bot = Bot(get_token(var))
    dp = Dispatcher()
    dp.include_router(form_router)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


FORM_FUNCS = {
    Form.start: start,
    Form.create: start_create,
    GameStates.run: choose_action,
    GameStates.inventory: inventory_handle,
    GameStates.talk: talk,
    GameStates.talk_with: talk,
    GameStates.trade: trade,
    GameStates.trade_list: trade_list,
    GameStates.save_menu: save_menu,
    GameStates.remove_save_menu: remove_save_menu,
    GameStates.choose_location: choose_location,
}


if __name__ == "__main__":
    bot_token: str = "GAME_BOT_TOKEN"
    asyncio.run(main(bot_token))
