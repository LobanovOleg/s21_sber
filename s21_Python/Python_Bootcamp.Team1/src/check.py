import asyncio
from dotenv import load_dotenv  # type: ignore
import logging
from aiogram import Dispatcher, Bot, F, Router  # type: ignore
from aiogram.filters import CommandStart  # type: ignore
from aiogram.types import (  # type: ignore
    Message,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.context import FSMContext  # type: ignore
from aiogram.fsm.state import State, StatesGroup  # type: ignore
from naming_bot import create_keyboard, get_token, create_name, PERSONS
import character_classes as c
import load_data as ld
import fill_data as fd
import tables as t
import game_bot_buttons as b
from uuid import uuid4
import time
import os
import copy
import argparse
import random as r
import all_maps  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from typing import Dict, List, Union, Any, Optional


load_dotenv()
form_router = Router()


class Form(StatesGroup):
    start = State()
    create = State()
    input_name = State()
    choose_class = State()
    choose_appearance = State()
    generate = State()
    start_game = State()
    null = State()


"""
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


class GameStates(StatesGroup):
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
    tic_tac_toe = State()


"""
"attack"   | "up"        | "talk"  |
"left"     | "inventory" | "right" |
"whereami" | "down"      | "saves" |

"attack" | GameStates.run
    "Имена врагов" | GameStates.attack
        "Атаковать снова" | GameStates.attack
            В случае смерти
            "Последнее сохранение"
            "Выбрать сохранение"
            "Выход"
        "Уйти"
    "Назад"

"""

DATA: Dict[str, Any] = {
    "init": {
        "name": "",
        "class_name": "",
        "appearance": "",
        "appearances": ["🧑🏻", "👨🏼", "🥷", "🤴", "👨🏻‍🦰"],
    },
    "hero": c.Protagonist("null"),
    "map_free": "⬜️🟨",
    "traces": {},
}
PLAYABLE_CLS: Dict[str, int] = {
    "Кондотьер ⚔️": c.ClassID.CONDOTR,
    "Корсар ☠️": c.ClassID.CORSAIR,
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
        GameStates.attack_enemy: GameStates.run,
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
    fields: List[List[List[str]]] = load_fields()
    await state.update_data(fields=fields)
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
    keys = [KeyboardButton(text=pc) for pc in PLAYABLE_CLS] + [b.BACK_BTN]
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
    keys = [
        KeyboardButton(text=i)
        for i in DATA["init"]["appearances"] + [b.BACK_BTN]
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

    values: List[int] = list(PLAYABLE_CLS.values())
    class_id = c.r.randint(min(values), max(values))
    init = DATA["init"]
    init["class_name"] = "".join(
        [k for k, v in PLAYABLE_CLS.items() if v == class_id]
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
            init["name"] is None
            or init["class_name"] is None
            or init["appearance"] is None
        ):
            if init["name"] is None:
                error = "Имя не задано"
            elif init["class_name"] is None:
                error = "Класс не задан"
            elif init["appearance"] is None:
                error = "Внешность не задана"
            raise ValueError(error)
        DATA["hero"] = c.Protagonist(
            name=init["name"],
            class_id=PLAYABLE_CLS[init["class_name"]],
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
async def load_game(message: Message, state: FSMContext):
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
        class_id = PLAYABLE_CLS.get(inp, None)
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
        if inp in "appearance":
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
        DATA = ld.loader(DATA, drop_db=args.drop)
        await state.update_data(start_time=time.time())
        if DATA["characters"] is None:
            raise ValueError("NPC не загружены")
        if DATA["phrases"] is None:
            raise ValueError("Диалоги не загружены")
        await state.set_state(GameStates.run)
        text = "Волны хлещут о берег... 🏝"
        keys = [KeyboardButton(text="Осмотреться")]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


def load_fields() -> List[List[List[str]]]:
    fields: List[List[List[str]]] = []
    map_dir = os.getenv("CVC_MAP")
    if map_dir is None:
        raise ValueError("CVC_MAP environment variable did not set")

    for m in all_maps.maps:
        text = m.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
    return fields


def get_map(location: str) -> List[List[List[str]]]:
    fields: List[List[List[str]]] = []
    map_dir = os.getenv("CVC_MAP")
    HERO: c.Protagonist = DATA["hero"]
    if map_dir is None:
        raise ValueError("CVC_MAP environment variable did not set")
    if location == "🏔 Первая северная локация":
        text = all_maps.map_2.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 2
    elif location == "🏞 Вторая северная локация":
        text = all_maps.map_3.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 3
    elif location == "🏕 Третья северная локация":
        text = all_maps.map_4.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 4
    elif location == "🏖 Первая южная локация":
        text = all_maps.map_5.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 5
    elif location == "🏜 Вторая южная локация":
        text = all_maps.map_6.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 6
    elif location == "🏝 Третья южная локация":
        text = all_maps.map_7.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 7
    elif location == "🏙 Первая восточная локация":
        text = all_maps.map_8.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 8
    elif location == "🏞 Вторая восточная локация":
        text = all_maps.map_9.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 9
    elif location == "🏕 Третья восточная локация":
        text = all_maps.map_10.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 10
    elif location == "🏞 Первая западная локация":
        text = all_maps.map_11.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 11
    elif location == "🏔 Вторая западная локация":
        text = all_maps.map_12.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 12
    elif location == "🏕 Третья западная локация":
        text = all_maps.map_13.split("\n")[1:-1]
        fields.append([[c for c in row] for row in text])
        HERO.location_id = 13
    else:
        raise ValueError("Неизвестная локация")
    return fields


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

    st_data: Dict[str, Any] = await state.get_data()
    hero = DATA["hero"]
    lid: int = hero.location_id
    field: List[List[str]] = st_data["fields"][lid - 1]
    npc_walking(lid, field)
    new_dir: c.Direction = hero.whereami()
    try:
        new_dir = go_handle(hero, msg.text, field)
        text: str = "Топ-топ"
    except ValueError:
        text = "Туда не пройти"
    await msg.answer(text, reply_markup=await create_keyboard(b.GAME_BTNS, 3))
    await pursuit_handle(msg, state, new_dir)


def npc_walking(lid, field) -> None:
    npcs = [
        npc
        for npc in DATA["characters"]["NPC"] + DATA["characters"]["Enemy"]
        if npc.location_id == lid
    ]

    for npc in npcs:
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
            try:
                go_handle(npc, direct, field)
            except ValueError:
                pass


def go_handle(person, direction, field) -> c.Direction:
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
    person.go(new_dir) if is_correct_pos(field, new_dir) else None
    return new_dir


async def pursuit_handle(msg, state, new_dir) -> None:
    for enemy in DATA["pursuit"]:
        enemy.pursuit_time -= 1
        if enemy.pursuit_time > 0:
            chance: int = r.randint(0, 1)
            if not is_in_range(enemy, 1) and chance:
                pos = enemy.whereami()
                if new_dir.y > pos.y:
                    pos = c.Direction(pos.x, pos.y + 1)
                elif new_dir.y < pos.y:
                    pos = c.Direction(pos.x, pos.y - 1)
                elif new_dir.x > pos.x:
                    pos = c.Direction(pos.x + 1, pos.y)
                elif new_dir.x < pos.x:
                    pos = c.Direction(pos.x - 1, pos.y)
                enemy.go(pos)
            if is_in_range(enemy, enemy.weapon.range):
                text = f"Вас догнал {enemy.name}\n"
                text += DATA["hero"].attack(enemy)
                await msg.answer(text)
                if text == c.DEFEAT:
                    await die(msg, state)
        else:
            DATA["pursuit"].remove(enemy)


def is_correct_pos(field: List[List[str]], new_dir: c.Direction) -> bool:
    is_correct: bool = False
    y_max: int = len(field) - 1
    if_y: bool = new_dir.y <= y_max and new_dir.y >= 0
    if_x: bool = False
    if if_y:
        if_x = new_dir.x >= 0 and new_dir.x <= len(field[new_dir.y]) - 1
    if (
        if_x
        and if_y
        and field[y_max - new_dir.y][new_dir.x] in DATA["map_free"]
    ):
        is_correct = True
    if not is_correct:
        raise ValueError()
    return is_correct


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
    hero = DATA["hero"]
    weapon_range: int = hero.weapon.range
    enemies: List[c.Enemy] = DATA["characters"]["Enemy"].copy()
    if hero.class_id == c.ClassID.CORSAIR:
        enemies += DATA["characters"]["NPC"]
    enemies_in_range: List[c.Enemy] = []
    for enemy in enemies:
        if enemy.hp > 0 and is_in_range(enemy, weapon_range):
            enemies_in_range.append(enemy)
    text: str = "Кого атаковать? 🗡"
    keys = [KeyboardButton(text=e.name) for e in enemies_in_range]
    keys = split_buttons(keys)
    await state.update_data(attack=enemies_in_range)
    await msg.answer(text, reply_markup=await create_keyboard(keys))


def is_in_range(npc: Union[c.NPC, c.Enemy], comparison: int) -> bool:
    """Returns whether NPC is in range of comparison with Protagonist

    Parameters
    ----------
    npc : c.NPC  |  c.Enemy]
        The given NPC

    comparison : int
        The comparison range

    Returns
    -------
    bool
        True if NPC in range
    """

    res: bool = False
    hero = DATA["hero"]
    if hero.location_id == npc.location_id:
        pos_h: c.Direction = hero.whereami()
        pos_n: c.Direction = npc.whereami()
        if (pos_h.x - pos_n.x) ** 2 + (
            pos_h.y - pos_n.y
        ) ** 2 <= comparison ** 2:
            res = True
    return res


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

    await state.set_state(GameStates.attack_enemy)
    cur_enemy: c.Enemy
    in_list: bool = False
    st_data: Dict[str, Any] = await state.get_data()
    enemies_in_range: List[c.Enemy] = st_data["attack"]
    inp: Optional[str] = msg.text
    for enemy in enemies_in_range:
        if inp and enemy.name in inp:
            cur_enemy = enemy
            in_list = True
            break
    await state.update_data(enemy=cur_enemy) if in_list else None
    await attack_enemy(msg, state)


@form_router.message(GameStates.attack_enemy)
async def attack_enemy(msg: Message, state: FSMContext):
    inp: Optional[str] = msg.text
    st_data: Dict[str, Any] = await state.get_data()
    enemy = st_data.get("enemy", st_data.get("npc", None))
    if inp == b.LOOT and enemy and enemy.hp <= 0:
        loot_enemy(enemy)
        await choose_action(msg, state)
    elif inp == b.ESCAPE:
        chance: int = r.randint(0, 1)
        if chance:
            await choose_action(msg, state)
        else:
            await hero_attack(msg, state, enemy, st_data)
    else:
        await hero_attack(msg, state, enemy, st_data)


async def hero_attack(
    msg: Message, state: FSMContext, enemy: c.Enemy, st_data: Dict[str, Any]
) -> None:
    text: str = DATA["hero"].attack(enemy)

    enemy.pursuit_time = 5
    if enemy not in DATA["pursuit"]:
        DATA["pursuit"].append(enemy)

    keys = [
        KeyboardButton(text=f"Атаковать снова {enemy.name} 🗡"),
        b.ESCAPE_BTN,
    ]
    if text.startswith(c.ENEMY_DEFEAT):
        keys = [b.LOOT_BTN, b.LEAVE_BTN]
        if enemy in DATA["characters"]["Enemy"]:
            DATA["characters"]["Enemy"].remove(enemy)
        elif enemy in DATA["characters"]["NPC"]:
            DATA["characters"]["NPC"].remove(enemy)

    if text == c.DEFEAT:
        await die(msg, state)
    else:
        await msg.answer(text, reply_markup=await create_keyboard(keys))


def loot_enemy(enemy):
    inventory = copy.deepcopy(enemy.inventory)
    for item, quantity in inventory.items():
        if item and item not in [DATA["std_weapon"], DATA["std_armor"]]:
            # if not item.is_tradable:
            #     table_type = t.Item if type(item) is t.Item else c.Weapon
            #     item = session.query(table_type).filter_by(
            #         name=item.name, is_tradable=True).first()
            for i in DATA["hero"].inventory:
                if i.name == item.name:
                    DATA["hero"].inventory[i] += quantity
                break


@form_router.message(GameStates.die)
async def die(msg, state) -> None:
    await state.set_state(GameStates.die)
    inp: Optional[str] = msg.text
    text = c.DEFEAT
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


@form_router.message(GameStates.run, F.text == b.BTNS_MEAN["whereami"])
async def show_whereami(msg: Message, state: FSMContext):
    """Show message that contains name, hp, position

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    """

    hero = DATA["hero"]
    text = get_hero_info(hero)
    pos: c.Direction = hero.whereami()
    text += f" находится на [{pos.x}, {pos.y}]\n"
    text += await show_map(msg, state)
    await msg.answer(text)
    await msg.answer(
        "Куда направлемся?", reply_markup=await create_keyboard(b.DIR_BTNS, 3)
    )
    await state.set_state(GameStates.choose_location.state)


async def show_map(msg: Message, state: FSMContext) -> str:
    hero: c.Protagonist = DATA["hero"]
    lid: int = hero.location_id
    pos: c.Direction
    st_data: Dict[str, Any] = await state.get_data()
    field = copy.deepcopy(st_data["fields"][lid - 1])
    y_max: int = len(field) - 1
    x_max = len(field[y_max])

    NPCs = DATA["characters"]["NPC"] + DATA["characters"]["Enemy"]

    for quest in [q for q in hero.questbook if not q.is_done]:
        if quest.kind == c.QuestKind.TRACE and quest.location_id == lid:
            quest_trace_handle(NPCs, quest, field, y_max)

    for npc in NPCs:
        pos = npc.whereami()
        if (
            npc.location_id == lid
            and npc.hp > 0
            and pos.x < x_max
            and pos.y < y_max
        ):
            field[y_max - pos.y][pos.x] = npc.appearance

    pos = hero.whereami()
    field[y_max - pos.y][pos.x] = hero.appearance

    text: str = ""
    for row in field:
        text += "".join(row)
        text += "\n"
    return text


def quest_trace_handle(NPCs, quest, field, y_max):
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


def make_trace(field, start, end, quest, y_max) -> None:
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
        new_pos = copy.deepcopy(start)
        DATA["traces"][quest.id].append(new_pos)
        field[y_max - start.y][start.x] = quest.item


@form_router.message(GameStates.choose_location)
async def choose_location(msg: Message, state: FSMContext):
    """Show message for wich location you can going

    Parametrs
    ---------
    msg: Message
        The message that caused the command to be executed
    state: FSMContext
        FSM state context
    """
    HERO: c.Protagonist = DATA["hero"]
    text = msg.text
    if text == b.DIR_BTNS_MEAN["North"]:
        await state.update_data(dir="North")
        await msg.answer(
            "В какую локацию севера?",
            reply_markup=await create_keyboard(b.NORTH_BTNS, 2),
        )
        await state.set_state(GameStates.choose_sub_loc.state)
    elif text == b.DIR_BTNS_MEAN["South"]:
        await state.update_data(dir="South")
        await msg.answer(
            "В какую локацию юга?",
            reply_markup=await create_keyboard(b.SOUTH_BTNS, 2),
        )
        await state.set_state(GameStates.choose_sub_loc.state)
    elif text == b.DIR_BTNS_MEAN["East"]:
        await state.update_data(dir="East")
        await msg.answer(
            "В какую локацию востока?",
            reply_markup=await create_keyboard(b.EAST_BTNS, 2),
        )
        await state.set_state(GameStates.choose_sub_loc.state)
    elif text == b.DIR_BTNS_MEAN["West"]:
        await state.update_data(dir="West")
        await msg.answer(
            "В какую локацию запада?",
            reply_markup=await create_keyboard(b.WEST_BTNS, 2),
        )
        await state.set_state(GameStates.choose_sub_loc.state)
    elif text == b.DIR_BTNS_MEAN["Begining"]:
        HERO.location_id = 1
        HERO.set_pos(0, 0)
        load_fields()
        await state.set_state(GameStates.run.state)
        await msg.answer(
            "Вы вернулись в начало",
            reply_markup=await create_keyboard(b.GAME_BTNS, 3),
        )
        await choose_action(msg, state)
    else:
        await msg.answer("Выберите направление.")


@form_router.message(GameStates.choose_sub_loc)
async def choose_sub_loc(msg: Message, state: FSMContext):
    """Show message for wich subloc you can going

    Parametrs
    ---------
    msg: Message
        The message that caused the command to be executed
    state: FSMContext
        FSM state context
    """
    HERO: c.Protagonist = DATA["hero"]
    inp: Optional[str] = msg.text
    data = await state.get_data()
    dir = data.get("dir")

    if dir == "North":
        loc_buttons_mean = b.NORTH_BTNS_MEAN
    elif dir == "South":
        loc_buttons_mean = b.SOUTH_BTNS_MEAN
    elif dir == "East":
        loc_buttons_mean = b.EAST_BTNS_MEAN
    elif dir == "West":
        loc_buttons_mean = b.WEST_BTNS_MEAN
    else:
        loc_buttons_mean = {}

    if inp and inp in loc_buttons_mean.values():
        fields: List[List[List[str]]] = get_map(inp)
        HERO.set_pos(0, 0)
        await state.update_data(fileds=fields)
        await state.set_state(GameStates.run.state)
        await msg.answer(
            f"Вы попали в {inp}",
            reply_markup=await create_keyboard(b.GAME_BTNS, 3),
        )
        await choose_action(msg, state)
    else:
        await msg.answer("Выберите локацию")


def get_hero_info(hero) -> str:
    cls_name: str = "".join(
        [name for name, v in PLAYABLE_CLS.items() if v == hero.class_id]
    )
    text: str = (
        f"{cls_name} {hero.level} lvl {hero.name} {hero.appearance} "
        f"[{hero.hp} ❤️]"
    )
    return text


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
    text: str = get_hero_info(hero) + "\n"
    div_len: int = 20
    text += "_" * div_len + "\n"

    text += "\nТекущее оружие\n"
    wpn = hero.weapon
    text += f"{wpn.name} {wpn.dmg_min}-{wpn.dmg_max} 🗡, {wpn.range} 🎯\n"

    text += "\nТекущая одежда\n"
    armor = hero.armor
    text += f"{armor.name} {armor.buff} 🛡\n"
    text += "_" * div_len + "\n"

    text += "\nВ инвентаре:\n"
    weaponry = []
    armory = []
    for item, quantity in hero.inventory.items():
        if type(item) is c.Item and item != DATA["std_armor"]:
            if item.buff_parameter == fd.ItemBuff.DEFENSE:
                armory.append(item)
            else:
                text += f"{item.name}: {quantity} шт.\n"
        elif type(item) is c.Weapon and item != DATA["std_weapon"]:
            weaponry.append(item)

    for w in weaponry:
        text += (
            f"{w.name}: урон {w.dmg_min}-{w.dmg_max} 🗡, "
            f"дальность {w.range} 🎯\n"
        )
    for a in armory:
        text += f"{a.name}: защита {a.buff}\n"
    keys = split_buttons(
        [
            b.SHOW_QUESTS_BTN,
            b.USE_BTN,
            b.CHOOSE_WEAPON_BTN,
            b.CHOOSE_ARMOR_BTN,
            b.THROW_OUT_BTN,
        ]
    )
    await msg.answer(text, reply_markup=await create_keyboard(keys))


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
            if type(w) is c.Weapon:
                keys.append(KeyboardButton(text=w.name))
        text = "Выберите оружие:"
    elif inp == b.CHOOSE_ARMOR:
        await state.set_state(GameStates.choose_armor)
        for a in hero.inventory:
            if type(a) is c.Item and a.buff_parameter == fd.ItemBuff.DEFENSE:
                keys.append(KeyboardButton(text=a.name))
        text = "Выберите одежду:"
    elif inp == b.THROW_OUT or inp == b.USE:
        for item in hero.inventory:
            if item not in [
                DATA["std_armor"],
                DATA["std_weapon"],
                hero.weapon,
                hero.armor,
            ]:
                keys.append(KeyboardButton(text=item.name))
        if inp == b.THROW_OUT:
            await state.set_state(GameStates.throw)
        elif inp == b.USE:
            await state.set_state(GameStates.use)
    elif inp == b.SHOW_QUESTS:
        await state.set_state(GameStates.show_quests)
        text = "Выберите квест:"
        keys = [
            KeyboardButton(text=q.brief)
            for q in hero.questbook
            if not q.is_done
        ]
    else:
        text = ""
        await show_inventory(msg, state)
    keys = split_buttons(keys)
    if text:
        await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.show_quests)
async def show_quests(msg: Message, state: FSMContext) -> None:
    inp: Optional[str] = msg.text
    text: str = ""
    keys: List[KeyboardButton] = []
    hero = DATA["hero"]
    if inp == "Выбрать другой квест 🔄":
        text = "Выберите квест:"
        keys = split_buttons(
            [KeyboardButton(text=q.brief) for q in hero.questbook]
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
    """Use the item

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
    if item_name not in [i.name for i in items]:
        text: str = "Такого предмета нет"
        await msg.answer(text, reply_markup=ReplyKeyboardRemove())
        await inventory_handle(msg, state)
    else:
        text = "Выбрано"
        text += "\n" + len(text) * "_" + "\n"
        for item in items:
            if item.name == item_name and item.buff:
                if item.buff_parameter == fd.ItemBuff.HP:
                    hero.heal(item.buff)
                elif item.buff_parameter == fd.ItemBuff.HP:
                    hero.weapon.dmg_min += item.buff
                    hero.weapon.dmg_max += item.buff
                hero.inventory[item] -= 1
                if hero.inventory[item] == 0:
                    del hero.inventory[item]
                break
                text += item.name
        await msg.answer(text, reply_markup=ReplyKeyboardRemove())
        await state.set_state(GameStates.inventory)
        await inventory_handle(msg, state)


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
        if type(w) is c.Weapon and inp and w.name in inp:
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
        if type(a) is c.Item:
            if (
                a.buff_parameter == fd.ItemBuff.DEFENSE
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
    inv = hero.inventory
    inp: Optional[str] = msg.text
    if msg.text == b.ALL:
        reduce = inv[item]
    elif inp:
        reduce = int(inp)
    quantity = inv[item]
    if quantity > reduce:
        inv[item] -= reduce
    else:
        if hero.weapon == item:
            hero.weapon = [w for w in inv if w.name == "Кулаки"][0]
        elif hero.armor == item:
            hero.armor = [a for a in inv if a.name == "Голое тело"][0]
        del inv[item]
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
    npcs: List[c.NPC] = DATA["characters"]["NPC"] + DATA["characters"]["Enemy"]
    talk_range: int = 2
    npcs_in_range: List[c.NPC] = []
    for npc in npcs:
        if npc.hp > 0 and is_in_range(npc, talk_range):
            npcs_in_range.append(npc)
    text: str = "С кем поговорить? 🗣"
    keys = [KeyboardButton(text=n.name) for n in npcs_in_range]
    keys = split_buttons(keys)
    await state.update_data(talk=npcs_in_range)
    await msg.answer(text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.talk)
async def talk_menu(msg: Message, state: FSMContext):
    """Talk bimenu

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
        keys = [b.TALK_WITH_BTN, b.TRADE_BTN, b.INSPECT_BTN, b.BACK_BTN]
        await msg.answer(text, reply_markup=await create_keyboard(keys))


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
        if npc not in DATA["characters"]["Enemy"]:
            await state.set_state(GameStates.trade)
            await trade(msg, state)
        else:
            text: str = "С ним не получится торговать"
            keys = [b.BACK_BTN]
            await msg.answer(text, keys=await create_keyboard(keys))
    elif inp == b.INSPECT:
        cls_name: str = "".join(
            [name for name, v in PLAYABLE_CLS.items() if v == npc.class_id]
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
    text = answer["phrase"]
    keys = [KeyboardButton(text=r) for r in answer["responses"]]
    ends = [
        c.Phrases.END_CIV.value,
        c.Phrases.END_CON.value,
        c.Phrases.END_COR.value,
    ]
    angry_ends = [c.Phrases.ANGRY_END_CON.value, c.Phrases.ANGRY_END_COR.value]
    quest_ends = [
        c.Phrases.GRATITUDE_CIV.value,
        c.Phrases.GRATITUDE_CON.value,
        c.Phrases.GRATITUDE_CON.value,
        c.Phrases.UPSET_CIV.value,
        c.Phrases.UPSET_CON.value,
        c.Phrases.UPSET_COR.value,
    ]
    is_end: str = ""
    for end in ends + angry_ends + quest_ends:
        if text in end:
            if text in angry_ends:
                is_end = "angry"
            elif text == "Давай сыграем":
                is_end = "play"
            else:
                is_end = "ordinary"
            break
    await msg.answer(
        text, parse_mode="HTML", reply_markup=await create_keyboard(keys)
    )

    if is_end == "ordinary":
        await check_quests(msg, npc)
        await choose_action(msg, state)
    elif is_end == "angry":
        await state.set_state(GameStates.attack_enemy)
        await attack_enemy(msg, state)
    elif is_end == "play":
        if npc.questbook and npc.questbook[0].kind == c.QuestKind.TIC_TAC_TOE:
            await play_tic_tac_toe(msg, state, npc)


async def play_tic_tac_toe(msg, state, npc) -> None:
    await state.set_state(GameStates.tic_tac_toe)
    text: str = "Первым ходит"
    field: List[List[str]] = [[" " * 3] * 3]
    chance: int = r.randint(0, 1)
    if chance:
        text += "е вы"
        await state.update_data(ttt_player="X")
        await state.update_data(ttt_npc="O")
    else:
        text += f" {npc.name}"
        await state.update_data(ttt_npc="X")
        await state.update_data(ttt_player="O")
        row: int = r.randint(0, 2)
        col: int = r.randint(0, 2)
        field[row][col] = "X"
    keys: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=c, callback_data=f"{y} {x}")
            for x, c in enumerate(row)
        ]
        for y, row in enumerate(field)
    ]
    await state.update_data(turn=chance)
    await state.update_data(ttt_field=field)
    await msg.answer(text, reply_markup=await create_keyboard(keys))


def check_end_tic_tac_toe(field, player: str, npc: str):
    is_end: int = 0
    for i in range(len(field)):
        row = []
        for j in range(len(field[i])):
            row.append(field[i][j])
            if j == 0:
                col = [field[k][j] for k in range(len(field))]
                if all([c == player or c == npc for c in col]):
                    is_end = 1 if field[i][j] == player else -1
                    break
        if all([c == player or c == npc for c in row]):
            is_end = 1 if field[i][j] == player else -1
            break
    return is_end


@form_router.message(GameStates.tic_tac_toe)
async def tic_tac_toe_round(msg, state) -> None:
    inp: Optional[str] = msg.text
    st_data: Dict[str, Any] = await state.get_data()
    field: List[List[str]] = st_data["ttt_field"]
    player: str = st_data["ttt_player"]
    npc: str = st_data["ttt_npc"]
    npc_obj: c.NPC = st_data["npc"]
    is_end = check_end_tic_tac_toe(field, player, npc)
    if is_end:
        text: str = "Вы победили" if is_end == 1 else f"{npc_obj.name} победил"
        keys: List[Any] = [
            KeyboardButton(text="Сыграть еще раз"),
            KeyboardButton(text="Бывай"),
        ]
        await state.set_state(GameStates.dialogue)
    else:
        turn = st_data["turn"]
        text = "Выберите клетку:"
        if turn and inp:
            turn = 0
            row, col = [int(i) for i in inp.split()]
            if field[row][col] == " ":
                field[row][col] = player
        elif turn == 0:
            turn = 1
            text += f"{npc_obj.name} сходил"
            row = r.randint(0, 2)
            col = r.randint(0, 2)
            if field[row][col] == " ":
                field[row][col] = npc
        await state.set_state(turn=turn)
        keys = [
            [
                InlineKeyboardButton(text=c, callback_data=f"{y} {x}")
                for x, c in enumerate(row)
            ]
            for y, row in enumerate(field)
        ]
    await msg.answer(text, reply_markup=await create_keyboard(keys))


async def check_quests(msg, npc):
    hero = DATA["hero"]
    for quest in [q for q in hero.questbook if not q.is_done]:
        if (
            quest.giving_npc_id
            and npc.id == quest.giving_npc_id
            or quest.receiving_npc_id
            and npc.id == quest.receiving_npc_id
        ):
            if eval(quest.condition):
                await quest_accept(msg, hero, quest)


async def quest_accept(msg, hero, quest) -> None:
    text = hero.advance_exp(quest.reward)
    if quest.kind == c.QuestKind.DELIVERY:
        items = [i for i in DATA["items"] if i.name == quest.item]
        if items:
            item = items[0]
            hero.throw(item)
    if quest.reward_item and quest.reward_item_quantity:
        items = [
            i
            for i in DATA["items"] + DATA["weapons"]
            if i.name == quest.reward_item
        ]
        if items:
            item = items[0]
            qnt: int = quest.reward_item_quantity
            hero.inventory[item] = qnt
            text += f"\n Вы получили {qnt} шт. {item.name}"
    quest.is_done = True
    await msg.answer(text)


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
    st_data : Dict[str, Any]
        The state dictionary
    trade_type : str
        Buy or sell
    hor_width : int
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
        text += "Выбранные товары персонажа:"
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
    cost : int
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
                if item.name == "Пиастра":
                    text += str(quantity)
                    text += cost_naming(quantity)
                else:
                    text += f"{item.name}: {item.cost}"
                    text += cost_naming(item.cost)
                    if quantity > 1:
                        text += f" (Осталось {quantity} шт.)"
                text += "\n"
                keys += [KeyboardButton(text=item.name)]
    keys = split_buttons(keys + [b.DONE_BTN])
    await msg.answer(text, reply_markup=await create_keyboard(keys))


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
            if type(item) is c.Item or type(item) is c.Weapon:
                npc.give(hero, item, quantity)
        for item, quantity in st_data["sell"].items():
            if type(item) is c.Item or type(item) is c.Weapon:
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
                break
        await state.update_data(item=item_found)

        text = "Введите количество"
        available_quantity -= st_data.get(trade_type, {}).get(item_found, 0)
        keys: List[KeyboardButton] = []
        if available_quantity is not None:
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
    item = st_data["item"]
    trade_type = st_data["trade"]

    trade_dict = st_data.get(trade_type, {})
    trade_dict.setdefault(item, 0)
    if quantity < 0:
        available_quantity = trade_dict[item]
        available_quantity += quantity
        quantity -= available_quantity if available_quantity < 0 else 0
    else:
        person = st_data["npc"] if trade_type == "buy" else DATA["hero"]
        inventory: Dict[Union[c.Item, c.Weapon], int] = person.inventory

        available_quantity = [q for i, q in inventory.items() if i == item][0]
        available_quantity -= trade_dict.get(item, 0)
        available_quantity -= quantity
        quantity += available_quantity if available_quantity < 0 else 0

    trade_dict[item] += quantity
    trade_dict["sum"] += item.cost * quantity

    await state.set_state(GameStates.trade)
    await trade(msg, state)


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
    session: Session = ld.get_session()
    await state.update_data(session=session)

    save_ids: List[int] = []
    hero = DATA["hero"]
    if hero is not None:
        save_ids = [
            p.save_id
            for p in session.query(t.Person).filter_by(id=hero.id).all()
        ]
    await state.update_data(save_ids=save_ids)
    if inp == b.QUICK_LOAD or inp == b.QUICK_SAVE:
        if not len(save_ids) and inp == b.QUICK_LOAD:
            text: str = "Нет сохранений!"
            keys = [b.BACK_BTN]
            await msg.answer(text, reply_markup=await create_keyboard(keys))
        elif inp == b.QUICK_LOAD:
            await load(msg, state, max(save_ids), session)
        elif inp == b.QUICK_SAVE:
            t_save = (
                session.query(t.Save)
                .filter(
                    t.Save.id.in_(save_ids),
                    t.Save.description.like(f"%{b.QUICK_SAVE}%"),
                )
                .first()
            )
            if t_save:
                session.delete(t_save)
                session.commit()
                session.close()
            session = ld.get_session()
            await save(msg, state, session)
    elif inp == b.LOAD:
        await load_choose(msg, state, hero.id)
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
    session = st_data.get("session", ld.get_session())
    await save(msg, state, session)


async def save(msg: Message, state: FSMContext, session: ld.Session):
    """Saves the game process to tables

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    session : ld.Session
    """

    inp: str = msg.text if msg.text else ""
    save_ids = session.query(t.Save.id).order_by(t.Save.id.desc()).first()
    save_id = 1 if save_ids is None else save_ids[0] + 1
    st_data: Dict[str, Any] = await state.get_data()
    cur_time: float = time.time() - st_data.get("start_time", 0)
    game_time = (
        f"{cur_time // 3600}:{(cur_time % 3600) // 60}:{round(cur_time % 60)}"
    )
    description = inp + " " + game_time + " | SAVE ID " + str(save_id)

    session.add(t.Save(id=save_id, description=description, time=cur_time))
    session.commit()
    hero = DATA["hero"]
    await save_person(session, save_id, hero)
    for npc in DATA["characters"]["NPC"] + DATA["characters"]["Enemy"]:
        await save_person(session, save_id, npc)

    session.commit()

    text: str = "Сохранение...\nЗагружайся по uuid ⬇️!\n"
    await msg.answer(text, reply_markup=ReplyKeyboardRemove())
    await msg.answer(text=hero.id)
    await choose_action(msg, state)


async def save_person(
    session: ld.Session,
    save_id: int,
    person: Union[c.Protagonist, c.NPC, c.Enemy],
) -> None:
    """Save Protagonits and NPCs to tables

    Parameters
    ----------
    session : ld.Session
        The PostgreSQL session
    save_id : int
        The current save_id
    person : Union[c.Protagonist, c.NPC, c.Enemy]
        The character class
    """

    t_person = t.Person()
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
                continue
            setattr(t_person, attr, value)
    for item, quantity in person.inventory.items():
        if type(item) is c.Item:
            t_person.items.append(
                t.Person_Item(
                    person_id=person.id,
                    save_id=save_id,
                    item_id=item.id,
                    quantity=quantity,
                )
            )
        elif type(item) is c.Weapon:
            t_person.weapons.append(
                t.Person_Weapon(
                    person_id=person.id, save_id=save_id, weapon_id=item.id
                )
            )
    for quest in person.questbook:
        t_person.quests.append(
            t.Person_Quest(
                person_id=person.id,
                save_id=save_id,
                quest_id=quest.id,
                is_done=quest.is_done,
            )
        )
    session.add(t_person)
    session.commit()


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
        await load_choose(msg, state, inp)


def parsing_arguments():
    parser = argparse.ArgumentParser(
        "Write -drop if database has been changed"
    )
    parser.add_argument(
        "-d",
        "--drop",
        action="store_true",
        help="drops corsairs_vs_condottiers database",
    )
    return parser.parse_args()


async def load_choose(msg: Message, state: FSMContext, hero_id: str):
    """Choose load st_data from saves

    Parameters
    -------
    ---
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    hero_id : str
        The protagonist id needed to take save ids
    """

    args = parsing_arguments()
    is_new: bool = ld.create_db_and_user(args.drop)
    session: Session = ld.get_session()
    await state.update_data(session=session)
    if is_new:
        fd.fill_database(session)

    ids = session.query(t.Person.save_id).filter_by(id=DATA["hero"].id).all()
    ids = [id[0] for id in ids]
    saves = session.query(t.Save.description).filter(t.Save.id.in_(ids)).all()
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
        save_id: int = int(inp.split()[-1])
        st_data: Dict[str, Any] = await state.get_data()
        session = st_data.get("session", ld.get_session())
        await load(msg, state, save_id, session)


async def load(
    msg: Message, state: FSMContext, save_id: int, session: ld.Session
) -> None:
    """Returns game status from load st_data

    Parameters
    ----------
    msg : Message
        The message that caused the command to be executed
    state : FSMContext
        FSM state context
    save_id : int
        The Save table id
    session : ld.Session
        The PostgreSQL session

    Raises
    ------
    ValueError
        If save doesn't exist by given save_id
    """

    save = session.query(t.Save).filter_by(id=save_id).first()
    if save is None:
        raise ValueError("Не существует сохранения с таким ID")
    st_data: Dict[str, Any] = await state.get_data()
    is_init_load: bool = st_data.get("is_init_load", False)
    global DATA
    DATA = ld.loader(DATA, save_id=save_id, is_init_load=is_init_load)
    await state.update_data(is_init_load=False)
    await state.update_data(start_time=save.time)
    text: str = "Загрузка..."
    await msg.answer(text, reply_markup=ReplyKeyboardRemove())
    await choose_action(msg, state)


@form_router.message(GameStates.remove_save_menu)
async def remove_save_menu(msg: Message, state: FSMContext):
    st_data: Dict[str, Any] = await state.get_data()
    save_ids = st_data["save_ids"]
    session: Session = st_data["session"]
    if save_ids:
        await state.set_state(GameStates.remove_save)
        text: str = "Выберите сохранение, которое хотите удалить:"
        saves = session.query(t.Save).filter(t.Save.id.in_(save_ids)).all()
        keys = [KeyboardButton(text=s.description) for s in saves]
        keys = split_buttons(keys)
    else:
        text = "Сохранений нет"
        await state.set_state(GameStates.remove_save_menu)
        keys = [b.BACK_BTN]
    await msg.answer(text=text, reply_markup=await create_keyboard(keys))


@form_router.message(GameStates.remove_save)
async def remove_save(msg: Message, state: FSMContext):
    description: Optional[str] = msg.text
    st_data: Dict[str, Any] = await state.get_data()
    save_ids = st_data["save_ids"]
    saves: List[t.Save] = []
    session: Session = st_data["session"]
    if save_ids:
        saves = session.query(t.Save).filter(t.Save.id.in_(save_ids)).all()
    if description in [s.description for s in saves]:
        save = session.query(t.Save).filter_by(description=description).first()
        if save:
            save_ids.remove(save.id)
            await state.update_data(save_ids=save_ids)
            session.delete(save)
            session.commit()
    await remove_save_menu(msg, state)


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


@form_router.message(F.text == b.EXIT)
async def exit_game(msg: Message, state: FSMContext):
    hero = DATA["hero"]
    if hero is None:
        raise ValueError("Персонаж не создан")
    text: str = f"Волны тихо плещутся о берег...\nID {hero.id}"
    await msg.answer(text)


async def main(var: str) -> None:
    """Starts the bot's event processing using aiogram.

    Parameters
    ----------
    var : str
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
}


if __name__ == "__main__":
    bot_token: str = "GAME_BOT_TOKEN"
    asyncio.run(main(bot_token))
