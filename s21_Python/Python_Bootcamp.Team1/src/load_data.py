"""The module loads all game characters from PostgreSQL database

Module requires character_classes to use game characters,
tables - to use ORM table models, fill_data - to fill database tables
if the database has not yet been created, sqlalchemy - to work with the
PostgreSQL database, uuid4 - to generate a unique identifier for
protagonist, os and dotenv to load environment variables
"""

import character_classes as c
import tables as t
import fill_data as fd
from sqlalchemy import URL, create_engine, text  # type: ignore
from sqlalchemy.orm import Session, sessionmaker  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from uuid import uuid4
import os
from dotenv import load_dotenv  # type: ignore
from typing import Dict, Any, Union

load_dotenv()

SQL_ARGS = {
    "base": os.getenv("CVC_NAME", "NULL"),
    "host": os.getenv("CVC_HOST", "NULL"),
    "port": os.getenv("CVC_PORT", "NULL"),
    "user": os.getenv("CVC_USER", "NULL"),
    "pass": os.getenv("CVC_PASS", "NULL"),
}


def loader(
    data: Dict[str, Any], save_id=1, drop_db=False, is_init_load=False
) -> Dict[str, Any]:
    """Loads non-playable characters from database

    Parameters
    ----------
    hero : c.Protagonist
        The created protagonist

    save_id : int, optional
        Load with modified parameters from saves or not

    drop_db : bool, optional
        Need or not drop database (for example if tables changed)

    Returns
    -------
    Dict[str, Any]
        The dictionary with all characters
    """

    is_new: bool = create_db_and_user(drop_db)

    session = get_session()

    if is_new:
        fd.fill_database(session)

    hero = data["hero"]
    if save_id == 1 or is_init_load:
        data["items"] = [
            copy_attr(c.Item(), i) for i in session.query(t.Item).all()
        ]
        data["weapons"] = [
            copy_attr(c.Weapon(), w) for w in session.query(t.Weapon).all()
        ]
        data["quests"] = [
            copy_attr(c.Quest(), q) for q in session.query(t.Quest).all()
        ]

    if save_id == 1:
        add_std_equipment(hero, data)
    else:
        t_hero = (
            session.query(t.Person)
            .filter_by(id=hero.id, save_id=save_id)
            .first()
        )
        if t_hero:
            copy_persons(hero, t_hero)
            add_inventory_and_weapon(hero, t_hero, data)

    armor_name: str = (
        "Стальной нагрудник"
        if hero.class_id == c.ClassID.CONDOTR
        else "Кожаный камзол"
    )
    armors = [i for i in data["items"] if i.name == armor_name]
    if armors:
        armor = armors[0]
        hero.inventory[armor] = 1
        hero.armor = armor
    data["hero"] = hero

    characters: Dict[str, Any] = {"NPC": [], "Enemy": []}
    data["pursuit"] = []

    NPCs = (
        session.query(t.Person)
        .filter_by(save_id=save_id, is_protagonist=False)
        .all()
    )

    for npc in NPCs:
        if (
            hero.class_id == c.ClassID.CORSAIR
            and npc.class_id != c.ClassID.CONDOTR
        ) or (
            hero.class_id == c.ClassID.CONDOTR
            and npc.class_id != c.ClassID.CORSAIR
        ):
            person = c.NPC()
        else:
            person = c.Enemy()
        copy_persons(person, npc)
        if save_id == 1 or is_init_load:
            add_std_equipment(person, data)
        add_inventory_and_weapon(person, npc, data)
        if type(person) is c.NPC:
            characters["NPC"].append(person)
        else:
            characters["Enemy"].append(person)

        if person.pursuit_time:
            data["pursuit"].append(person)

    session.close()
    data["phrases"] = get_phrases(characters)
    data["characters"] = characters
    return data


def create_db_and_user(drop_db) -> bool:
    """Checking the database and user, if doesn't exist, creates it

    Parameters
    ----------
    drop_db : bool, optional
        Need or not drop database

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

    url_object = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )
    eng = create_engine(url_object)

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

        if drop_db and is_exist:
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

    url_object = URL.create(
        "postgresql+psycopg2",
        username=SQL_ARGS["user"],
        password=SQL_ARGS["pass"],
        host=SQL_ARGS["host"],
        port=SQL_ARGS["port"],
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
    for attr, value in t_item.__dict__.items():
        if hasattr(item, attr):
            setattr(item, attr, value)
    return item


def copy_persons(
    person: Union[c.Protagonist, c.NPC, c.Enemy], t_person: t.Person
) -> None:
    for attr, value in t_person.__dict__.items():
        if attr == "_Person__pos":
            attr = "_Protagonist__pos"
        if hasattr(person, attr):
            if attr == "_Protagonist__pos":
                value = c.Direction(value[0], value[1])
            setattr(person, attr, value)


def add_std_equipment(
    person: Union[c.Protagonist, c.NPC, c.Enemy], data: Dict[str, Any]
) -> None:
    std_weapons = [w for w in data["weapons"] if w.name == "Кулаки"]
    if not std_weapons:
        raise ValueError("Item not in database")
    std_weapon = std_weapons[0]
    person.inventory[std_weapon] = 1
    person.weapon = std_weapon

    std_armors = [i for i in data["items"] if i.name == "Голое тело"]
    if not std_armors:
        raise ValueError("Item not in database")
    std_armor = std_armors[0]
    person.inventory[std_armor] = 1
    person.armor = std_armor

    std_coins = [i for i in data["items"] if i.name == "Пиастра"]
    if not std_armors:
        raise ValueError("Item not in database")
    std_coin = std_coins[0]
    person.inventory[std_coin] = 100

    data["std_weapon"] = std_weapon
    data["std_armor"] = std_armor
    data["std_coin"] = std_coin


def add_inventory_and_weapon(
    person: Union[c.Protagonist, c.NPC, c.Enemy],
    t_person: t.Person,
    data: Dict[str, Any],
) -> None:
    """Add items from tables Person_Item and Person_weapon

    Parameters
    ----------
    npcs : List[Union[c.NPC, c.Enemy]]
        The list of nonplayable characters
    session : Session
        The PostgreSQL session
    save_id : int
        The save id
    """

    for pair in t_person.items:
        items = [i for i in data["items"] if i.id == pair.item.id]
        if items:
            item: c.Item = items[0]
            person.inventory[item] = pair.quantity
            if item.buff_parameter == fd.ItemBuff.DEFENSE and (
                not hasattr(person, "armor") or item.buff > person.armor.buff
            ):
                person.armor = item
    for pair in t_person.weapons:
        weapons = [w for w in data["weapons"] if w.id == pair.weapon.id]
        if weapons:
            weapon = weapons[0]
            person.inventory[weapon] = 1
            if (
                not hasattr(person, "weapon")
                or weapon.dmg_min > person.weapon.dmg_min
            ):
                person.weapon = weapon

    hero_cls_id = data["hero"].class_id
    person.questbook = []
    for pair in t_person.quests:
        quests = [q for q in data["quests"] if q.id == pair.quest.id]
        if quests:
            quest = quests[0]
            if quest.class_id is None or hero_cls_id == quest.class_id:
                quest.is_done = pair.is_done
                person.questbook.append(quest)


def get_phrases(chrs) -> Dict[str, Any]:
    all_phrases = {
        c.Phrases.INIT.value: [
            {
                "text": (
                    "Что, кот? Какая кошка? [ <i>Приглушенное</i> Mяяяу ]"
                    "\n...Гм... аа, слышал, слышал\n"
                    "Передай письмо моему товарищу - Франческо Тотти,\n"
                    "он обычно бывает на западе, и приходи обратно"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Денис Риччи"
                    ][0].id
                    + ") and 'Следы кота' in [q.brief for q in self.questbook"
                    " if not q.is_done]"
                ),
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "Аа, письмо? [ <i>Пробегает глазами</i> ], спасибо "
                    "за весточку. Получи в награду от меня этот Кортик\n"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Франческо Тотти"
                    ][0].id
                    + ") and 'Письмо для сослуживца' in [q.brief"
                    " for q in self.questbook] and 'Письмо друга' "
                    "in [item.name for item in self.inventory]"
                ),
                "response": [
                    c.Phrases.WHATS_NEW.value,
                    c.Phrases.QUEST_NEW.value,
                    c.Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Передал письмо? Хорошо. Есть информация по твоему"
                    " коту, но сначала обыграй меня 😉"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Денис Риччи"
                    ][0].id
                    + ") and 'Письмо для сослуживца' in [q.brief for q in"
                    " self.questbook if q.is_done]"
                ),
                "response": [c.Phrases.LETS_PLAY.value, c.Phrases.END.value],
            },
            {
                "text": (
                    "Что? Говорят я украл кота короля? "
                    "[Звуки негодования...]\n"
                    "Это все происки гнусных кондотьеров\n"
                    "Передай это известие нашему товарищу Ризотто Неро\n"
                    "Его ты сможешь найти в третьей южной локации.\n"
                    "А я пока что-нибудь здесь придумаю."
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Омар Капоне"
                    ][0].id
                    + ") and 'Подстава' in [q.brief for q in self.questbook]"
                    " and 'Финальный бой' not in [q.brief for q in self.questbook]"
                    " and ('Сабля' and 'Стальной нагрудник') not in [item.name for item in self.inventory]"
                ),
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                    c.Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Оoo Друживщееее.. иккк.. буээ..\n"
                    "[Судя по всему это был тот самый пьяный из корсаров"
                    " - Ризотто Неро...]\n"
                    "Друживщее, ты кек равз ввреемяяя. Падайдии.. икфф"
                    ".. к Джамалу Корлеоне и папросии.. буээ икфф.. "
                    "у него еще вина\nОн тут где-то не подалеку"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Ризотто Неро"
                    ][0].id
                    + ") and 'Тот самый.. Ризотто Неро' in [q.brief for q in"
                    " self.questbook] and 'Сильнейший' not in [q.brief for q"
                    " in self.questbook] and 'Бутылка вина' not in"
                    " [item.name for item in self.inventory]"
                ),
                "response": [
                    "Ай да по бутылке вина!",
                    c.Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "Категорически приветствую!\n"
                    "[Перед тобой стоит один из генералов корсаров"
                    " - Джамал Корлеоне].\n"
                    "Что же хочет от меня такой молодой сослуживец?"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Джамал Корлеоне"
                    ][0].id
                    + ") and 'Бутылка вина' in [q.brief"
                    " for q in self.questbook]"
                ),
                "response": [
                    "Хочу попросить у Вас бутылку вина.",
                    c.Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Приветствую!\n"
                    "Я вижу ты смог справиться со своим испытанием!"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Месут Озил"
                    ][0].id
                    + ") and 'Испытание смелости' in [q.brief"
                    " for q in self.questbook] and 'Бутылка вина' "
                    "not in [item.name for item in self.inventory]"
                ),
                "response": ["Конечно справился!", c.Phrases.END.value],
            },
            {
                "text": (
                    "Оооо.. Ты вернулся. Да еще и с бутылкой вина..\n"
                    "Икффф.. буэээ..\n"
                    "Держи за это вот такой подарок"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Ризотто Неро"
                    ][0].id
                    + ") and 'Сильнейший' in [q.brief"
                    " for q in self.questbook] and 'Бутылка вина' "
                    "in [item.name for item in self.inventory]"
                ),
                "response": [
                    "Оу, премного благодарен за столь ценный подарок!"
                ],
            },
            {
                "text": (
                    "Здравствуй, друже!\n"
                    "Пьяница Ризотто предупредил насчет тебя\n"
                    "Что же получи свою награду"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Джорно Джованна"
                    ][0].id
                    + ") and 'Подготовка' in [q.brief for q in self.questbook]"
                    " and 'Сабля' in [item.name for item in self.inventory]"
                ),
                "response": ["Откуда у вас защита кондотьера?"],
            },
            {
                "text": (
                    "Эй дружище!\n"
                    "Рад тебя видеть снова! Вижу что ты смог найти виновного в клевете"
                    " и разобрался с ним. Так держать!"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        n
                        for n in chrs["NPC"] + chrs["Enemy"]
                        if n.name == "Омар Капоне"
                    ][0].id
                    + ") and 'Финальный бой' in [q.brief"
                    " for q in self.questbook] and 'Сабля' "
                    "in [item.name for item in self.inventory]"
                    " and 'Стальной нагрудник' in [item.name for item in self.inventory]"
                ),
                "response": [
                    "Спасибо за поздравления!",
                    c.Phrases.END.value
                ],
            },
            {
                "text": "Aве, гражданин!",
                "condition": "npc.class_id == ClassID.CIVIL",
                "response": [
                    c.Phrases.WHATS_NEW.value,
                    c.Phrases.QUEST_NEW.value,
                    c.Phrases.END.value,
                ],
            },
            {
                "text": "Aве, камрад!",
                "condition": (
                    "npc.class_id == ClassID.CONDOTR and type(npc) is not"
                    " Enemy"
                ),
                "response": [
                    c.Phrases.WHATS_NEW.value,
                    c.Phrases.QUEST_NEW.value,
                    c.Phrases.END.value,
                ],
            },
            {
                "text": "Эй, Дружище!",
                "condition": (
                    "npc.class_id == ClassID.CORSAIR and type(npc) is not"
                    " Enemy"
                ),
                "response": [
                    c.Phrases.WHATS_NEW.value,
                    c.Phrases.QUEST_NEW.value,
                    c.Phrases.END.value,
                ],
            },
            {
                "text": c.Phrases.ANGRY_END_CON.value,
                "condition": (
                    "npc.class_id == ClassID.CONDOTR and type(npc) is Enemy"
                ),
                "response": ["Никогда! Смерть или слава, приятель!"],
            },
            {
                "text": c.Phrases.ANGRY_END_COR.value,
                "condition": (
                    "npc.class_id == ClassID.CORSAIR and type(npc) is Enemy"
                ),
                "response": ["Может, попробуешь подкрепить слова делом?"],
            },
        ],
        c.Phrases.WHATS_NEW.value: [
            {
                "text": (
                    "Да вроде все по-прежнему в Датском королевстве...\n"
                    "Аа, ты уже слышал, что пропал кот короля?!\n"
                    "Говорят даже, что его украл капитан корсаров - Омар"
                    " Капоне!\nНо мало ли, что говорят люди"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        p.id
                        for p in chrs["NPC"]
                        if p.name == "Джованни Чичиков"
                    ][0]
                    + ") and self.class_id == ClassID.CONDOTR"
                ),
            },
            {
                "text": (
                    "Ах, корсар..\n"
                    "Да вроде все по-прежнему в Датском королевстве...\n"
                    "Слышал, что ваш капитан - Омар Капоне похитил кота"
                    "короля.\nИль же это все слухи?"
                ),
                "condition": (
                    "npc.id == str("
                    + [
                        p.id
                        for p in chrs["NPC"]
                        if p.name == "Джованни Чичиков"
                    ][0]
                    + ") and self.class_id == ClassID.CORSAIR"
                ),
                "response": ["Вздор! Это подстава!", c.Phrases.END.value],
            },
            {
                "text": "Ничего",
                "response": [c.Phrases.QUEST_NEW.value, c.Phrases.END.value],
            },
        ],
        c.Phrases.QUEST_NEW.value: [
            {
                "text": "У меня есть для тебя задание",
                "condition": "npc.questbook",
                "response": ["Говори", c.Phrases.END.value],
            },
            {
                "text": "Да нет ничего",
                "condition": "npc.questbook is None",
                "response": [c.Phrases.WHATS_NEW.value, c.Phrases.END.value],
            },
        ],
        c.Phrases.END.value: [
            {
                "text": c.Phrases.END_CIV.value,
                "condition": "npc.class_id == ClassID.CIVIL",
            },
            {
                "text": c.Phrases.END_CON.value,
                "condition": "npc.class_id == ClassID.CONDOTR",
            },
            {
                "text": c.Phrases.END_COR.value,
                "condition": "npc.class_id == ClassID.CORSAIR",
            },
        ],
        "Вздор! Это подстава!": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Ай да по бутылке вина!": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                    c.Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Хочу попросить у Вас бутылку вина.": [
            {
                "text": "ЧТОО??!!\nБутылку вина? И для кого же она?",
                "response": [
                    "Для господина Ризотто Неро",
                    "Для меня достопочтенного!",
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Для господина Ризотто Неро": [
            {
                "text": (
                    "Ах.. Этому пьянице. Как ему не стыдно просить об этом"
                    " других!\nХмммм.. хмм..\nЧто же, я дам тебе бутылку при"
                    " одном условии\nТебе необходимо одолеть одного из"
                    " кондотьеров. После победы найди Месута Озила в первой"
                    " южной локации."
                ),
                "response": [
                    "Кого же?",
                    c.Phrases.REFUSE_QUEST.value,
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Кого же?": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                    c.Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Конечно справился!": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                    c.Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Для меня достопочтенного!": [
            {
                "text": (
                    "ЩЕЕЕЕНОК!\nТЫ ХОТЬ ПОНИМАЕШЬ У КОГО ТАКОЕ"
                    " ПРОСИШЬ?\nХМММ.. хмммм..\nЧто же наглец, я дам тебе"
                    " бутылку вина если ты одолеешь кое-кого!"
                ),
                "response": [
                    "Кто же это?",
                    c.Phrases.REFUSE_QUEST.value,
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Кто же это?": [
            {
                "text": "Одолей Макскорпоне Палаццо в третьей восточной локации",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                    c.Phrases.END.value,
                ],
            }
        ],
        "Оу, премного благодарен за столь ценный подарок!": [
            {
                "text": (
                    "Знаешь что? Икфф.. Направляйся к Джорно Джованне.\n"
                    "Он находится в третьей восточной локации."
                ),
                "response": ["Вперед!", c.Phrases.END.value],
            }
        ],
        "Вперед!": [
            {
                "text": (
                    "Отправляйся к Джорно Джованне в третью восточную локацию"
                ),
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                    c.Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Откуда у вас защита кондотьера?": [
            {
                "text": (
                    "Трофей достался [Джорно потирает ладони...]\nВсе наши"
                    " сослуживцы видят в тебе большой потенциал\nТак пойди же"
                    " и сокруши главного кондотьера - Винсента ван Гога\nЗА"
                    " КОРСАРОВ!!!"
                ),
                "response": ["Так тому и быть", c.Phrases.END.value],
            }
        ],
        "Так тому и быть": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                    c.Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Спасибо за поздравления!": [
            {
                "text": ("Теперь у вас есть удостоверение заслуженого корсара\n"
                         "Вы успешно прошли основной квест!\n"
                         "Желаете завершить игру или продолжить путешествие?"),
            }
        ],
        "Говори": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    c.Phrases.ACCEPT_QUEST.value,
                    c.Phrases.REFUSE_QUEST.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        c.Phrases.ACCEPT_QUEST.value: [
            {
                "text": c.Phrases.GRATITUDE_CIV.value,
                "condition": "npc.class_id == ClassID.CIVIL",
            },
            {
                "text": c.Phrases.GRATITUDE_CON.value,
                "condition": "npc.class_id == ClassID.CONDOTR",
            },
            {
                "text": c.Phrases.GRATITUDE_COR.value,
                "condition": "npc.class_id == ClassID.CORSAIR",
            },
        ],
        c.Phrases.REFUSE_QUEST.value: [
            {
                "text": c.Phrases.UPSET_CIV.value,
                "condition": "npc.class_id == ClassID.CIVIL",
            },
            {
                "text": c.Phrases.UPSET_CON.value,
                "condition": "npc.class_id == ClassID.CONDOTR",
            },
            {
                "text": c.Phrases.UPSET_COR.value,
                "condition": "npc.class_id == ClassID.CORSAIR",
            },
        ],
    }
    return all_phrases


if __name__ == "__main__":
    hero_name = "Пончик"
    hero_cls_id = c.ClassID.CONDOTR
    try:
        hero = c.Protagonist(str(uuid4()), hero_name, hero_cls_id)
        data: Dict[str, Any] = {"hero": hero}
        data = loader(data)
        for corsair in data["characters"]["Enemy"]:
            print(
                corsair.name,
                corsair.inventory,
                corsair.hp,
                corsair.weapon.dmg_max,
            )
    except ValueError as e:
        print(f"Error: {e}")
