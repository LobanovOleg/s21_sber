"""The module loads all game characters from PostgreSQL database

Module requires sqlalchemy - to work with the PostgreSQL database,
uuid4 - to generate a unique identifier for protagonist, os and dotenv
to load environment variables, copy - to deepcopy quests for different,
persons, character_classes to use game characters, tables - to use ORM
table models, fill_data - to fill database tables, if the database has
not yet been created, phrases - to load player and character lines
"""

from sqlalchemy import URL, create_engine, text  # type: ignore
from sqlalchemy.orm import Session, sessionmaker  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from uuid import uuid4
import os
from dotenv import load_dotenv  # type: ignore
import copy
import json
import character_classes as c
import tables as t
import fill_data as fd
from phrases import get_phrases
from typing import Dict, List, Any, Union, Optional
from argparse import Namespace

load_dotenv()

SQL_ARGS = {
    "base": os.getenv("CVC_NAME", "NULL"),
    "host": os.getenv("CVC_HOST", "NULL"),
    "port": os.getenv("CVC_PORT", "NULL"),
    "user": os.getenv("CVC_USER", "NULL"),
    "pass": os.getenv("CVC_PASS", "NULL"),
}


def loader(
    data: Dict[str, Any],
    save_id: int,
    args: Optional[Namespace],
    is_init_load: bool,
) -> Dict[str, Any]:
    """Loads all game data from PostgreSQL database

    Parameters
    ----------
    data: Dict[str, Any]
        Dictionary with init information
    save_id : int
        Load with modified parameters from saves or not
    args : Namespace
        Need or not drop database, change or append values,
    is_init_load : bool
        Is starts game from load
    Returns
    -------
    Dict[str, Any]
        The dictionary with all game needed data
    """

    is_new: bool = create_db_and_user(args)

    session = get_session()

    if is_new or (args and (args.correct or args.append)):
        fd.fill_database(session, args)

    if data.get("items", None) is None:
        data["items"] = [
            copy_attr(c.Item(), i) for i in session.query(t.Item).all()
        ]
    if data.get("weapons", None) is None:
        data["weapons"] = [
            copy_attr(c.Weapon(), w) for w in session.query(t.Weapon).all()
        ]
    if data.get("quests", None) is None:
        data["quests"] = [
            copy_attr(c.Quest(), q) for q in session.query(t.Quest).all()
        ]
    if any(
        x is None
        for x in [
            data.get("std_weapon", None),
            data.get("std_armor", None),
            data.get("std_coin", None),
        ]
    ):
        add_std_equipment(data)

    if is_init_load:
        add_std_equipment_to_person(data["hero"], data)
        add_init_armor(data["hero"], data)
    else:
        data["hero"] = c.Protagonist(id=data["hero"].id)
        t_hero = (
            session.query(t.Person)
            .filter_by(id=data["hero"].id, save_id=save_id)
            .first()
        )
        if t_hero:
            copy_persons(data["hero"], t_hero, data)
            add_items_buff(t_hero, data)
            add_items_weapons_quests(data["hero"], t_hero, data)

    characters: Dict[str, Any] = {"NPC": [], "Enemy": []}

    NPCs = (
        session.query(t.Person)
        .filter_by(save_id=save_id, is_protagonist=False)
        .all()
    )

    for npc in NPCs:
        if (
            data["hero"].class_id == c.ClassID.CORSAIR
            and npc.class_id != c.ClassID.CONDOTR
        ) or (
            data["hero"].class_id == c.ClassID.CONDOTR
            and npc.class_id != c.ClassID.CORSAIR
        ):
            person = c.NPC()
        else:
            person = c.Enemy()
        if is_init_load:
            add_std_equipment_to_person(person, data)
        copy_persons(person, npc, data)
        add_items_weapons_quests(person, npc, data)
        if type(person) is c.NPC:
            characters["NPC"].append(person)
        else:
            characters["Enemy"].append(person)

    session.close()
    data["phrases"] = get_phrases(characters)
    data["npcs"] = characters["NPC"]
    data["enemies"] = characters["Enemy"]
    data["news"] = get_news()
    return data


def create_db_and_user(args: Optional[Namespace]) -> bool:
    """Checking the database and user, if doesn't exist, creates it

    Parameters
    ----------
    args : Optional[Namespace]
        The command line arguments

    Raises
    ------
    ValueError
        If CVC environment variables didn't set

    Returns
    -------
    bool
        True if database created
    """

    if not all([value != "NULL" for value in SQL_ARGS.values()]):
        raise ValueError("Created database environment variables did not set")

    is_new: bool = False

    port: int = 5432
    if SQL_ARGS["port"]:
        port = int(SQL_ARGS["port"])

    url_object = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=port,
        database=os.getenv("DB_NAME"),
    )

    try:
        eng = create_engine(url_object)
    except BaseException:
        raise ValueError("postgresql error")

    with eng.connect().execution_options(isolation_level="AUTOCOMMIT") as con:
        is_exist = con.execute(
            text(f"SELECT 1 FROM pg_user WHERE usename = '{SQL_ARGS['user']}'")
        ).fetchone()
        if not is_exist:
            con.execute(
                text(
                    f"CREATE USER {SQL_ARGS['user']} "
                    f"WITH PASSWORD '{SQL_ARGS['pass']}'"
                )
            )

        is_exist = con.execute(
            text(
                "SELECT 1 FROM pg_database WHERE datname "
                f"= '{SQL_ARGS['base']}'"
            )
        ).fetchone()

        create_db_text = text(
            f"CREATE DATABASE {SQL_ARGS['base']} OWNER {SQL_ARGS['user']}"
        )

        if args and args.drop and is_exist:
            con.execute(text(f"DROP DATABASE {SQL_ARGS['base']};"))
            con.execute(create_db_text)
            is_new = True

        if not is_exist:
            con.execute(create_db_text)
            is_new = True

    eng.dispose()
    return is_new


def get_session() -> Session:
    """Returns session from session factory

    Returns
    -------
    Type[Session]
        Returns PostgreSQL sessions
    """

    port: int = 5432
    if SQL_ARGS["port"]:
        port = int(SQL_ARGS["port"])

    url_object = URL.create(
        "postgresql+psycopg2",
        username=SQL_ARGS["user"],
        password=SQL_ARGS["pass"],
        host=SQL_ARGS["host"],
        port=port,
        database=SQL_ARGS["base"],
    )
    engine: Engine = create_engine(url_object)
    t.Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return session_factory()


def copy_attr(
    item: Union[c.Item, c.Weapon, c.Quest],
    t_item: Union[t.Item, t.Weapon, t.Quest],
) -> Union[c.Item, c.Weapon, c.Quest]:
    """Copy attributes from ORM models to game classes

    Parameters
    ----------
    item : Union[c.Item, c.Weapon, c.Quest]
        Game class
    t_item : Union[t.Item, t.Weapon, t.Quest]
        ORM model

    Returns
    -------
    Union[c.Item, c.Weapon, c.Quest]
        Copied game class
    """

    for attr, value in t_item.__dict__.items():
        if hasattr(item, attr):
            setattr(item, attr, value)
    return item


def copy_persons(
    person: Union[c.Protagonist, c.NPC, c.Enemy],
    t_person: t.Person,
    data: Dict[str, Any],
) -> None:
    """Copy ORM person model to game person model

    Parameters
    ----------
    person : Union[c.Protagonist, c.NPC, c.Enemy]
        Game model
    t_person : t.Person
        ORM model
    data : Dict[str, Any]
        The loaded data from db
    """

    for attr, value in t_person.__dict__.items():
        if attr == "_Person__pos":
            attr = "_Protagonist__pos"
        if hasattr(person, attr):
            if attr == "_Protagonist__pos":
                value = c.Direction(value[0], value[1])
            elif attr == "weapon":
                values = [w for w in data["weapons"] if w.name == value]
                if not values:
                    value = data["std_weapon"]
                else:
                    value = values[0]
            elif attr == "armor":
                values = [
                    a
                    for a in data["items"]
                    if a.buff_parameter == c.ItemBuff.DEFENSE
                    and a.name == value
                ]
                if not values:
                    value = data["std_armor"]
                else:
                    value = values[0]
            setattr(person, attr, value)


def add_std_equipment(data: Dict[str, Any]) -> None:
    """Adds initial weapon, armor and items for person

    Parameters
    ----------
    data : Dict[str, Any]
        The loaded data from db

    Raises
    ------
    ValueError
        If any standart item not in database
    """

    std_weapons = [w for w in data["weapons"] if w.name == "Кулаки"]
    if not std_weapons:
        raise ValueError("Weapon not in database")
    data["std_weapon"] = std_weapons[0]

    std_armors = [i for i in data["items"] if i.name == "Голое тело"]
    if not std_armors:
        raise ValueError("Item not in database")
    data["std_armor"] = std_armors[0]

    std_coins = [i for i in data["items"] if i.name == "Пиастра"]
    if not std_armors:
        raise ValueError("Item not in database")
    data["std_coin"] = std_coins[0]


def add_std_equipment_to_person(
    person: Union[c.Protagonist, c.NPC, c.Enemy], data: Dict[str, Any]
) -> None:
    """Adds initial weapon, armor and items for person

    Parameters
    ----------
    person : Union[c.Protagonist, c.NPC, c.Enemy]
        The person to whom the items are issued
    data : Dict[str, Any]
        The loaded data from db
    """

    person.inventory[data["std_weapon"]] = 1
    person.weapon = data["std_weapon"]

    person.inventory[data["std_armor"]] = 1
    person.armor = data["std_armor"]

    person.inventory[data["std_coin"]] = 100


def add_init_armor(hero: c.Protagonist, data: Dict[str, Any]) -> None:
    """When initializing gives protagonist armor corresponding to class

    Parameters
    ----------
    hero : c.Protagonist
        The game's protagonist
    data : Dict[str, Any]
        Dictionary with init information
    """

    armor_name: str = (
        "Стальной нагрудник"
        if hero.class_id == c.ClassID.CONDOTR
        else "Кожаный камзол"
    )
    for i in data["items"]:
        if i.name == armor_name:
            hero.inventory[i] = 1
            hero.armor = i
            break


def add_items_weapons_quests(
    person: Union[c.Protagonist, c.NPC, c.Enemy],
    t_person: t.Person,
    data: Dict[str, Any],
) -> None:
    """Add items, weapons and quests from tables to person

    Parameters
    ----------
    person : Union[c.Protagonist, c.NPC, c.Enemy]
        The person to whom the things are issued
    t_person : t.Person
        The person's ORM model
    data : Dict[str, Any]
        The loaded data
    """

    t_items: List[t.Person_Item] = t_person.items if t_person.items else []
    for pair in t_items:
        item: Any = get_checked_thing(data["items"], pair, "item")
        if item and type(item) is c.Item:
            person.inventory[item] = pair.quantity

    t_weapons: List[t.Person_Weapon] = []
    if t_person.weapons:
        t_weapons = t_person.weapons
    for pair in t_weapons:
        weapon: Any = get_checked_thing(data["weapons"], pair, "weapon")
        if weapon and type(weapon) is c.Weapon:
            person.inventory[weapon] = 1

    hero_cls_id = data["hero"].class_id
    person.questbook = []

    t_quests: List[t.Person_Quest] = t_person.quests if t_person.quests else []
    for pair in t_quests:
        quest: Any = get_checked_thing(data["quests"], pair, "quest")
        if quest and type(quest) is c.Quest:
            if quest.class_id is None or hero_cls_id == quest.class_id:
                new_quest = copy.deepcopy(quest)
                new_quest.is_done = pair.is_done
                person.questbook.append(new_quest)


def add_items_buff(t_hero: t.Person, data: Dict[str, Any]) -> None:
    """Adds buff items

    Adds to data items that enhance the player and have not lost their
    effect at the time of saving

    Parameters
    ----------
    t_hero : t.Person
        The game's protagonist
    data : Dict[str, Any]
        The loaded data
    """

    data["items_duration"] = []
    t_buff_items: List[t.Person_BuffItem] = (
        t_hero.buff_items if t_hero.buff_items else []
    )
    for pair in t_buff_items:
        item: Any = get_checked_thing(data["items"], pair, "item")
        if item and type(item) is c.Item:
            data["items_duration"].append(item)


def get_checked_thing(
    things: Union[List[c.Item], List[c.Weapon], List[c.Quest]],
    pair: Union[
        t.Person_Item, t.Person_Weapon, t.Person_Quest, t.Person_BuffItem
    ],
    attr: str,
) -> Optional[Union[c.Item, c.Weapon, c.Quest]]:
    """Creates a new list with check if attributes match

    Parameters
    ----------
    lst : List[Any]
        Incoming list
    pair : Union[t.Person_Item, t.Person_Weapon, t.Person_Quest]
        Checked value
    attr : str
        Defines pair type
    Returns
    -------
    List[Any]
        Outcome list
    """

    checked_thing: Optional[Union[c.Item, c.Weapon, c.Quest]] = None
    for thing in things:
        if hasattr(pair, attr):
            table_thing = getattr(pair, attr)
            if hasattr(table_thing, "id") and hasattr(thing, "id"):
                if table_thing.id == thing.id:
                    checked_thing = thing
                    break
    return checked_thing


def get_news() -> Dict[str, str]:
    news: Dict[str, str] = {}
    env_var: str = "CVC_NEWS"
    file = os.getenv(env_var)
    if file is None:
        raise ValueError(f"{env_var} environment variable did not set")

    with open(file) as fp:
        news = json.load(fp)
    return news


if __name__ == "__main__":
    hero_name = "Пончик"
    hero_cls_id = c.ClassID.CONDOTR
    try:
        hero = c.Protagonist(str(uuid4()), hero_name, hero_cls_id)
        data: Dict[str, Any] = {"hero": hero}
        save_id: int = 1
        args: Optional[Namespace] = None
        is_init_load: bool = False
        data = loader(data, save_id, args, is_init_load)
        for corsair in data["enemies"]:
            print(
                corsair.name,
                corsair.inventory,
                corsair.hp,
                corsair.weapon.dmg_max,
            )
    except ValueError as e:
        print(f"Error: {e}")
