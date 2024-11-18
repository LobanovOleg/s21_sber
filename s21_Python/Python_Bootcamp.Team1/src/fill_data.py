"""The script fill database tables

Script requires tables to link the specified data with ORM models,
Session - to add data to the correct PostgreSQL session,
character_classes - to select the correct class identifier, quest kinds
and item boost parameters, logging - to handle with mistakes
"""

import tables as t
from sqlalchemy.orm import Session  # type: ignore
from character_classes import INIT_HP, ClassID, QuestKind, ItemBuff
import logging
from typing import List, Any, Optional
from argparse import Namespace


def fill_database(session: Session, args: Optional[Namespace]) -> None:
    """Fill databases with start values

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[argparse.Namespace]
        The command line arguments
    """

    fill_saves(session, args)
    fill_classes(session, args)
    fill_persons(session, args)
    fill_items(session, args)
    fill_weapons(session, args)

    def get_range(name_1: str, name_2: str, type: str) -> range:
        """Getting a range of ids for a specific game class

        Parameters
        ----------
        name_1: str
            Name of the first representative in the range
        name_2: str
            Name of the last representative in the range
        type: str
            Specific game class name
        """

        part_1: Optional[t.Person] = None
        part_2: Optional[t.Person] = None
        part_1 = session.query(t.Person).filter_by(name=name_1).first()
        part_2 = session.query(t.Person).filter_by(name=name_2).first()
        type_range = range(1)
        if part_1 and part_2 and part_1.id and part_2.id:
            type_range = range(int(part_1.id), int(part_2.id))
            logging.info(f"{type} range {type_range}")
        else:
            logging.info(f"{type} range query incorrect")
        return type_range

    name_start: str = "Джованни Чичиков"
    name_end: str = "Альфредо ди Стефано"
    civils_id: range = get_range(name_start, name_end, "civils")

    name_start = "Денис Риччи"
    name_end = "Владимир Мартини"
    condattieri_id: range = get_range(name_start, name_end, "condottieri")

    name_start = "Ахмед Флойд"
    name_end = "Сулейман Линч"
    corsairs_id: range = get_range(name_start, name_end, "corsairs")

    fill_persons_items(session, args, civils_id, condattieri_id, corsairs_id)
    fill_persons_weapons(session, args)
    fill_quests(session, args)
    fill_persons_quests(session, args)


def fill_saves(session: Session, args: Optional[Namespace]) -> None:
    """Fill classes table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line arguments
    """

    saves = [t.Save(id=1, description="Новая игра | SAVE ID 1", time=0)]
    args_handle(session, args, t.Save, saves)
    if (args and not args.correct) or not args:
        session.add_all(saves)
    session.commit()


def args_handle(
    session: Session, args: Optional[Namespace], table: Any, lst: List[Any]
) -> None:
    """Appends or corrects data in PostgreSQL db without deleting

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line argument
    table : Any
        Any table type
    lst : List[Any]
        List of any ORM models
    """

    recs: List[Any] = []
    SID: int = 1
    if args and (args.correct or args.append):
        if hasattr(table, "save_id"):
            recs = session.query(table).filter_by(save_id=SID).all()
        else:
            recs = session.query(table).all()

    remove_items: List[Any] = []
    if args and args.append:
        compare: List[Any] = [get_compare_elem(table, r) for r in recs]
        for item in lst:
            if get_compare_elem(table, item) in compare:
                remove_items.append(item)

    for item in remove_items:
        lst.remove(item)

    if args and args.correct:
        i: int = 0
        j: int = 0
        len_i: int = len(lst)
        len_j: int = len(recs)
        while i < len_i:
            if j < len_j and (
                get_compare_elem(table, recs[j])
                == get_compare_elem(table, lst[i])
            ):
                for attr, value in lst[i].__dict__.items():
                    if (
                        not attr.startswith("_sa")
                        and attr != "id"
                        and getattr(lst[i], attr) != getattr(recs[j], attr)
                    ):
                        setattr(recs[j], attr, value)
                j = len_j
            else:
                j += 1
            if j >= len_j:
                i += 1
                j = 0


def get_compare_elem(table: Any, elem: Any) -> Any:
    """Gets ORM model's comparator

    Parameters
    ----------
    table : Any
        Any table type
    elem : Any
        Any ORM model
    """

    cmp_elem: Any = 0
    if table == t.Quest:
        cmp_elem = elem.class_id, elem.description
    elif table == t.Person:
        cmp_elem = elem.name
    elif table == t.Person_Item:
        cmp_elem = elem.person_id, elem.item_id
    elif table == t.Person_Weapon:
        cmp_elem = elem.person_id, elem.weapon_id
    elif table == t.Person_Quest:
        cmp_elem = elem.person_id, elem.quest_id
    elif table == t.Item:
        cmp_elem = elem.name, elem.is_tradable
    else:
        cmp_elem = elem.id
    return cmp_elem


def fill_classes(session: Session, args: Optional[Namespace]) -> None:
    """Fill classes table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line argument
    """

    lst = [
        t.Class(id=ClassID.CIVIL, name="Мирный житель"),
        t.Class(id=ClassID.CONDOTR, name="Кондотьер"),
        t.Class(id=ClassID.CORSAIR, name="Корсар"),
    ]

    args_handle(session, args, t.Class, lst)
    if (args and not args.correct) or not args:
        session.add_all(lst)
    session.commit()


def fill_persons(session: Session, args: Optional[Namespace]) -> None:
    """Fill persons table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line argument
    """

    persons: List[t.Person] = []
    SID: int = 1
    ID: int = 1

    def add_person(
        cid: ClassID, ico: str, name: str, lvl: int, lid: int, pos: List[int]
    ) -> t.Person:
        """Append person to persons ORM list

        Parameters
        ----------
        cid: ClassID
            The person's ClassID
        ico: str
            The person's appearance
        name: str
            The person's name
        lvl: int
            The person's level
        lid: int
            The person's start location ID
        pos: List[int]
            The person's position

        Returns
        -------
        t.Person
            Created person
        """

        nonlocal ID
        person = t.Person(
            id=str(ID), class_id=cid, save_id=SID, appearance=ico
        )
        ID += 1
        person.name = name
        person.level = lvl
        person.location_id = lid
        person._Person__pos = pos  # type: ignore
        person.hp = INIT_HP + lvl * 5 if INIT_HP else lvl * 5
        return person

    def add_special_weapon_armor(weapon=None, armor=None):
        """Add specific weapon and/or armor for unique person

        Parameters
        ----------
        weapon : str, optional
            The person's weapon
        armor : str, optional, by default None
            The person's armor, by default None
        """

        if persons:
            person = persons[-1]
            if weapon:
                person.weapon = weapon
            if armor:
                person.armor = armor

    def add_civ(
        name: str, lvl: int, lid: int, pos: List[int], ico="🙎‍♂️"
    ) -> None:
        """Append civil to persons ORM list

        Parameters
        ----------
        name: str
            The person's name
        lvl: int
            The person's level
        lid: int
            The person's start location ID
        pos: List[int]
            The person's position
        ico: str
            The person's appearance
        """

        person: t.Person = add_person(ClassID.CIVIL, ico, name, lvl, lid, pos)
        person.weapon = "Кулаки"
        person.armor = "Льняная рубашка"
        persons.append(person)

    # SORT BY LOCATION ID
    add_civ(name="Джованни Чичиков", lvl=1, lid=1, pos=[3, 2])
    add_special_weapon_armor(weapon="Парные пистоли")
    add_civ(name="Дидье Дешам", lvl=4, lid=1, pos=[14, 16])
    add_special_weapon_armor(weapon="Кортик")

    add_civ(name="Альберто Синичкин", lvl=2, lid=2, pos=[12, 13])
    add_special_weapon_armor(weapon="Кортик")
    add_civ(name="Андреа Пирло", lvl=1, lid=2, pos=[4, 3])

    add_civ(name="Никколо Романов", lvl=3, lid=3, pos=[1, 3])
    add_special_weapon_armor(weapon="Кортик")
    add_civ(name="Антонио Маргаретти", lvl=1, lid=3, pos=[6, 5])

    add_civ(name="Массимо Иванов", lvl=4, lid=4, pos=[1, 21])
    add_civ(name="Доминик де Кокко", lvl=1, lid=4, pos=[7, 6])

    add_civ(name="Франческо Горломи", lvl=2, lid=5, pos=[17, 0])
    add_civ(name="Джакомо Хаматдинов", lvl=4, lid=5, pos=[9, 4])
    add_special_weapon_armor(weapon="Парные пистоли")

    add_civ(name="Маттео Тапочкин", lvl=10, lid=6, pos=[7, 16], ico="🤴")
    add_special_weapon_armor(weapon="Парные пистоли")
    add_civ(name="Леонардо Макаров", lvl=3, lid=6, pos=[13, 15])
    add_special_weapon_armor(weapon="Парные пистоли")

    add_civ(name="Матео Ковачич", lvl=1, lid=7, pos=[8, 1])
    add_civ(name="Кристиан Харионов", lvl=4, lid=7, pos=[11, 3])

    add_civ(name="Олегос Лобановски", lvl=1, lid=8, pos=[8, 1])
    add_civ(name="Франчексо Соболев", lvl=4, lid=8, pos=[5, 16])

    add_civ(name="Роберто Стечкин", lvl=4, lid=9, pos=[4, 3])
    add_special_weapon_armor(weapon="Парные пистоли")

    add_civ(name="Кристофф Вальц", lvl=2, lid=10, pos=[13, 9])

    add_civ(name="Джанкарло Эспозито", lvl=3, lid=11, pos=[15, 1])
    add_special_weapon_armor(weapon="Парные пистоли")

    add_civ(name="Абригадо Тобакко", lvl=2, lid=12, pos=[19, 1])

    add_civ(name="Альфредо ди Стефано", lvl=1, lid=13, pos=[3, 2])

    def add_con(
        name: str, lvl: int, lid: int, pos: List[int], ico="💂🏼"
    ) -> None:
        """Append condottier to persons ORM list

        Parameters
        ----------
        name: str
            The person's name
        lvl: int
            The person's level
        lid: int
            The person's start location ID
        pos: List[int]
            The person's position
        ico: str
            The person's appearance
        """

        pers: t.Person = add_person(ClassID.CONDOTR, ico, name, lvl, lid, pos)
        pers.weapon = "Сабля"
        pers.armor = "Стальной нагрудник"
        persons.append(pers)

    add_con(name="Денис Риччи", lvl=3, lid=1, pos=[4, 13])
    add_con(name="Ильнур Коста", lvl=3, lid=1, pos=[13, 20])

    add_con(name="Франческо Тотти", lvl=2, lid=2, pos=[8, 15])
    add_con(name="Винсент ван Гог", lvl=3, lid=2, pos=[15, 4])

    add_con(name="Евпатий Коловрат", lvl=4, lid=3, pos=[7, 14])
    add_con(name="Александр Росси", lvl=2, lid=3, pos=[2, 7])

    add_con(name="Яромир Мендельсон", lvl=2, lid=4, pos=[0, 15])
    add_con(name="Федор Фабрици", lvl=4, lid=4, pos=[7, 9])

    add_con(name="Леонид Луккези", lvl=4, lid=5, pos=[11, 15])
    add_con(name="Иван Медичи", lvl=1, lid=5, pos=[16, 12])

    add_con(name="Соске Айдзен", lvl=4, lid=6, pos=[16, 5])
    add_special_weapon_armor(weapon="Ружье")
    add_con(name="Джанлуиджи Буффон", lvl=2, lid=6, pos=[12, 8])
    add_special_weapon_armor(weapon="Ружье")
    add_con(name="Клаудио Раньери", lvl=1, lid=6, pos=[3, 3])
    add_special_weapon_armor(weapon="Ружье")

    add_con(name="Северус Снейп", lvl=2, lid=7, pos=[19, 1])

    add_con(name="Марко Ройс", lvl=2, lid=8, pos=[8, 8])

    add_con(name="Маскарпоне Палаццо", lvl=4, lid=10, pos=[16, 1])
    add_con(name="Руслан да Сан Северино", lvl=2, lid=10, pos=[9, 13])

    add_con(name="Массимилиано Аллегри", lvl=1, lid=11, pos=[16, 9])
    add_con(name="Николай Сфорца", lvl=2, lid=11, pos=[5, 7])

    add_con(name="Олег Пальмери", lvl=4, lid=12, pos=[5, 8])

    add_con(name="Кенпачи Дзараки", lvl=3, lid=13, pos=[9, 20])
    add_con(name="Владимир Мартини", lvl=4, lid=13, pos=[12, 5])

    def add_cor(name: str, lvl: int, lid: int, pos: List[int], ico="👳🏼‍♂️"):
        """Append corsair to persons ORM list

        Parameters
        ----------
        name: str
            The person's name
        lvl: int
            The person's level
        lid: int
            The person's start location ID
        pos: List[int]
            The person's position
        ico: str
            The person's appearance
        """

        pers: t.Person = add_person(ClassID.CORSAIR, ico, name, lvl, lid, pos)
        pers.weapon = "Топор"
        pers.armor = "Кожаный камзол"
        persons.append(pers)

    add_cor(name="Ахмед Флойд", lvl=3, lid=1, pos=[16, 10])
    add_cor(name="Хобутус Плутович", lvl=1, lid=1, pos=[3, 25])

    add_cor(name="Терез Мей", lvl=4, lid=2, pos=[17, 20])

    add_cor(name="Жозе Моуриньо", lvl=2, lid=3, pos=[14, 10])

    add_cor(name="Генрих V", lvl=4, lid=4, pos=[15, 12])
    add_cor(name="Жан Пьер", lvl=1, lid=4, pos=[10, 3])

    add_cor(name="Месут Озил", lvl=1, lid=5, pos=[0, 3])
    add_cor(name="Али Клайд", lvl=2, lid=5, pos=[1, 6])

    add_cor(name="Ризотто Неро", lvl=4, lid=7, pos=[13, 13])
    add_cor(name="Джамал Корлеоне", lvl=2, lid=7, pos=[7, 7])

    add_cor(name="Мустафа Романо", lvl=3, lid=8, pos=[16, 3])
    add_cor(name="Гвидо Миста", lvl=3, lid=8, pos=[16, 11])

    add_cor(name="Мартин Лютер", lvl=2, lid=9, pos=[15, 13])
    add_cor(name="Карим Кастилия", lvl=3, lid=9, pos=[7, 12])
    add_cor(name="Салим Воробей", lvl=4, lid=9, pos=[7, 14])
    add_cor(name="Доппио Дьяволо", lvl=6, lid=9, pos=[10, 13], ico="👲🏼")
    add_special_weapon_armor(weapon="Пистоли")

    add_cor(name="Джорно Джованна", lvl=1, lid=10, pos=[4, 5])
    add_cor(name="Ашраф Леони", lvl=3, lid=10, pos=[9, 15])

    add_cor(name="Самир Вендетта", lvl=2, lid=11, pos=[14, 27])

    add_cor(name="Ибрагим Паша", lvl=3, lid=12, pos=[6, 20])
    add_cor(name="Омар Капоне", lvl=3, lid=12, pos=[6, 16])

    add_cor(name="Майк Тайсон", lvl=4, lid=13, pos=[14, 16])
    add_cor(name="Сулейман Линч", lvl=2, lid=13, pos=[5, 15])

    for person in persons:
        setattr(person, "is_protagonist", False)
    args_handle(session, args, t.Person, persons)
    if (args and not args.correct) or not args:
        session.add_all(persons)
    session.commit()


def fill_items(session: Session, args: Optional[Namespace]) -> None:
    """Fill items table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line argument
    """

    items: List[t.Item] = []
    items.append(
        t.Item(
            name="Пиастра",
            description="Золотая монета, местная валюта",
            is_tradable=True,
            cost=1,
        )
    )
    # hats
    items.append(
        t.Item(
            name="Берет", description="Берет мирного жителя", is_tradable=False
        )
    )
    items.append(
        t.Item(
            name="Берет",
            description="Берет мирного жителя",
            is_tradable=True,
            cost=5,
        )
    )

    items.append(
        t.Item(
            name="Красная шляпа",
            buff_parameter=ItemBuff.DAMAGE,
            buff=3,
            description="Шляпа кондотьера",
            is_tradable=False,
        )
    )
    items.append(
        t.Item(
            name="Красная шляпа",
            buff_parameter=ItemBuff.DAMAGE,
            buff=3,
            description="Шляпа кондотьера",
            is_tradable=True,
            cost=10,
        )
    )

    items.append(
        t.Item(
            name="Черная шляпа",
            buff_parameter=ItemBuff.HP,
            buff=2,
            description="Шляпа корсара",
            is_tradable=False,
        )
    )
    items.append(
        t.Item(
            name="Черная шляпа",
            buff_parameter=ItemBuff.HP,
            buff=2,
            description="Шляпа корсара",
            is_tradable=True,
            cost=10,
        )
    )

    items.append(
        t.Item(
            name="Зеленая шляпа",
            buff_parameter=ItemBuff.HP,
            buff=5,
            description="Шляпа корсара-главаря",
            is_tradable=False,
        )
    )
    items.append(
        t.Item(
            name="Зеленая шляпа",
            buff_parameter=ItemBuff.HP,
            buff=5,
            description="Шляпа корсара-главаря",
            is_tradable=True,
            cost=50,
        )
    )

    # clothes
    bp: int = ItemBuff.DEFENSE
    armors = []
    armors.append(
        t.Item(
            name="Голое тело",
            buff_parameter=bp,
            buff=0,
            description="Без одежды",
            is_tradable=False,
        )
    )

    armors.append(
        t.Item(
            name="Кожаный камзол",
            buff_parameter=bp,
            buff=5,
            description="Одежда корсара",
            is_tradable=False,
        )
    )
    armors.append(
        t.Item(
            name="Кожаный камзол",
            buff_parameter=bp,
            buff=5,
            description="Одежда корсара",
            is_tradable=True,
            cost=50,
        )
    )

    armors.append(
        t.Item(
            name="Стальной нагрудник",
            is_tradable=False,
            buff_parameter=bp,
            buff=10,
            description="Защита кондотьера",
        )
    )
    armors.append(
        t.Item(
            name="Стальной нагрудник",
            is_tradable=True,
            buff_parameter=bp,
            buff=10,
            description="Защита кондотьера",
            cost=70,
        )
    )

    armors.append(
        t.Item(
            name="Льняная рубашка",
            is_tradable=False,
            buff_parameter=bp,
            buff=1,
            description="Простая одежда",
        )
    )
    armors.append(
        t.Item(
            name="Льняная рубашка",
            is_tradable=True,
            buff_parameter=bp,
            buff=1,
            description="Простая одежда",
            cost=20,
        )
    )

    for a in armors:
        a.is_armor = True
    items += armors

    # special
    items.append(t.Item(name="Карта с кладом", is_tradable=False))
    items.append(
        t.Item(
            name="Удостоверение",
            buff_parameter=ItemBuff.DAMAGE,
            buff=1,
            description="Удостоверение кондотьера",
            is_tradable=False,
            is_usable=True
        )
    )

    # quest
    items.append(t.Item(name="Письмо друга", is_tradable=False))
    items.append(t.Item(name="Бутылка вина", is_tradable=False))
    items.append(
        t.Item(name="Удостоверение заслуженного корсара", is_tradable=False)
    )
    items.append(
        t.Item(
            name="Кот короля",
            description=(
                "Тот самый кот. Интересно, что вы с ним чувствуете себя"
                " гораздо более защищенным"
            ),
            buff_parameter=ItemBuff.DEFENSE,
            buff=7,
            is_tradable=False,
        )
    )

    for i in items:
        i.is_usable = False

    # food
    usable = []
    usable.append(
        t.Item(
            name="Ром",
            buff_parameter=ItemBuff.DAMAGE,
            buff=3,
            description="Любимый напиток корсара",
            duration=5,
            is_tradable=True,
            cost=3,
        )
    )
    usable.append(
        t.Item(
            name="Вино",
            buff_parameter=ItemBuff.HP,
            buff=1,
            buff_reusable=True,
            description="Любимый напиток жителя",
            duration=5,
            is_tradable=True,
            cost=3,
        )
    )
    usable.append(
        t.Item(
            name="Пиво",
            buff_parameter=ItemBuff.DEFENSE,
            buff=3,
            description="Любимый напиток кондотьера",
            duration=5,
            is_tradable=True,
            cost=3,
        )
    )
    usable.append(
        t.Item(
            name="Мешок с мукой",
            buff_parameter=ItemBuff.DEFENSE,
            buff=4,
            description="Можно сделать печеньки",
            duration=4,
            is_tradable=True,
            cost=4,
        )
    )
    usable.append(
        t.Item(
            name="Вяленое мясо",
            buff_parameter=ItemBuff.HP,
            buff=5,
            is_tradable=True,
            cost=4,
            description="Питательная пища",
        )
    )
    usable.append(
        t.Item(
            name="Галеты",
            buff_parameter=ItemBuff.HP,
            buff=3,
            description="Питательная пища",
            is_tradable=True,
            cost=2,
        )
    )
    usable.append(
        t.Item(
            name="Жареная рыба",
            buff_parameter=ItemBuff.HP,
            buff=4,
            is_tradable=True,
            cost=3,
            description="Питательная пища",
        )
    )

    for i in usable:
        i.is_usable = True

    items += usable

    args_handle(session, args, t.Item, items)
    if (args and not args.correct) or not args:
        session.add_all(items)
    session.commit()


def fill_weapons(session: Session, args: Optional[Namespace]) -> None:
    """Fill weapons table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line argument
    """

    weapons: List[t.Weapon] = []

    text: str = "Кулаки"
    weapons.append(
        t.Weapon(name=text, range=1, dmg_min=0, dmg_max=1, is_tradable=False)
    )
    text = "Кортик"
    weapons.append(
        t.Weapon(
            name=text, range=1, dmg_min=0, dmg_max=2, is_tradable=True, cost=10
        )
    )
    weapons.append(
        t.Weapon(name=text, range=1, dmg_min=0, dmg_max=2, is_tradable=False)
    )
    text = "Топор"
    weapons.append(
        t.Weapon(
            name=text, range=1, dmg_min=3, dmg_max=5, is_tradable=True, cost=20
        )
    )
    weapons.append(
        t.Weapon(name=text, range=1, dmg_min=3, dmg_max=5, is_tradable=False)
    )
    text = "Сабля"
    weapons.append(
        t.Weapon(
            name=text, range=1, dmg_min=4, dmg_max=6, is_tradable=True, cost=20
        )
    )
    weapons.append(
        t.Weapon(name=text, range=1, dmg_min=4, dmg_max=6, is_tradable=False)
    )

    text = "Пистоли"
    weapons.append(
        t.Weapon(
            name=text,
            range=10,
            dmg_min=4,
            dmg_max=6,
            is_tradable=True,
            cost=40,
        )
    )
    weapons.append(
        t.Weapon(name=text, range=10, dmg_min=4, dmg_max=6, is_tradable=False)
    )
    text = "Парные пистоли"
    weapons.append(
        t.Weapon(
            name=text,
            range=10,
            dmg_min=6,
            dmg_max=12,
            is_tradable=True,
            cost=80,
        )
    )
    weapons.append(
        t.Weapon(name=text, range=10, dmg_min=6, dmg_max=12, is_tradable=False)
    )
    text = "Ружье"
    weapons.append(
        t.Weapon(
            name=text,
            range=20,
            dmg_min=5,
            dmg_max=10,
            is_tradable=True,
            cost=140,
        )
    )
    weapons.append(
        t.Weapon(name=text, range=20, dmg_min=5, dmg_max=10, is_tradable=False)
    )
    args_handle(session, args, t.Weapon, weapons)
    if (args and not args.correct) or not args:
        session.add_all(weapons)
    session.commit()


def fill_persons_items(
    session: Session,
    args: Optional[Namespace],
    civ_id: range,
    con_id: range,
    cor_id: range,
) -> None:
    """Fill persons table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    civ_id : range
        The range of civilians id
    con_id : range
        The range of condottieri id
    cor_id : range
        The range of corsairs id
    """

    SID: int = 1
    civils: List[t.Person_Item] = []
    hat = (
        session.query(t.Item)
        .filter_by(name="Берет", is_tradable=False)
        .first()
    )
    cloth = (
        session.query(t.Item)
        .filter_by(name="Льняная рубашка", is_tradable=False)
        .first()
    )
    food = (
        session.query(t.Item)
        .filter_by(name="Вяленое мясо", is_tradable=True)
        .first()
    )
    alco = (
        session.query(t.Item).filter_by(name="Вино", is_tradable=True).first()
    )
    for i in civ_id:
        if hat and cloth and food and alco:
            civils.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=hat.id, quantity=1
                )
            )
            civils.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=cloth.id, quantity=1
                )
            )
            civils.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=food.id, quantity=1
                )
            )
            civils.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=alco.id, quantity=1
                )
            )

    item = (
        session.query(t.Item)
        .filter_by(name="Карта с кладом", is_tradable=False)
        .first()
    )
    (
        civils.append(
            t.Person_Item(
                person_id="1", save_id=SID, item_id=item.id, quantity=1
            )
        )
        if item
        else None
    )
    item = (
        session.query(t.Item).filter_by(name="Берет", is_tradable=True).first()
    )
    (
        civils.append(
            t.Person_Item(
                person_id="1", save_id=SID, item_id=item.id, quantity=1
            )
        )
        if item
        else None
    )

    condots: List[t.Person_Item] = []
    hat = (
        session.query(t.Item)
        .filter_by(name="Красная шляпа", is_tradable=False)
        .first()
    )
    cloth = (
        session.query(t.Item)
        .filter_by(name="Стальной нагрудник", is_tradable=False)
        .first()
    )
    food = (
        session.query(t.Item)
        .filter_by(name="Галеты", is_tradable=True)
        .first()
    )
    alco = (
        session.query(t.Item).filter_by(name="Пиво", is_tradable=True).first()
    )
    item = (
        session.query(t.Item)
        .filter_by(name="Удостоверение", is_tradable=False)
        .first()
    )
    for i in con_id:
        if hat and cloth and food and alco and item:
            condots.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=hat.id, quantity=1
                )
            )
            condots.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=cloth.id, quantity=1
                )
            )
            condots.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=food.id, quantity=1
                )
            )
            condots.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=alco.id, quantity=1
                )
            )
            condots.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=item.id, quantity=1
                )
            )

    alco = session.query(t.Item).filter_by(name="Ром").first()
    (
        condots.append(
            t.Person_Item(
                person_id="11", save_id=SID, item_id=alco.id, quantity=10
            )
        )
        if alco
        else None
    )

    corsairs: List[t.Person_Item] = []
    hat = (
        session.query(t.Item)
        .filter_by(name="Черная шляпа", is_tradable=False)
        .first()
    )
    cloth = (
        session.query(t.Item)
        .filter_by(name="Кожаный камзол", is_tradable=False)
        .first()
    )
    food = (
        session.query(t.Item)
        .filter_by(name="Жареная рыба", is_tradable=True)
        .first()
    )
    for i in cor_id:
        if hat and cloth and food and alco:
            corsairs.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=hat.id, quantity=1
                )
            )
            condots.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=cloth.id, quantity=1
                )
            )
            corsairs.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=food.id, quantity=1
                )
            )
            corsairs.append(
                t.Person_Item(
                    person_id=str(i), save_id=SID, item_id=alco.id, quantity=1
                )
            )

    item = (
        session.query(t.Item)
        .filter_by(name="Зеленая шляпа", is_tradable=False)
        .first()
    )
    (
        corsairs.append(
            t.Person_Item(
                person_id="30", save_id=SID, item_id=item.id, quantity=11
            )
        )
        if item
        else None
    )

    item = (
        session.query(t.Item)
        .filter_by(name="Кот короля", is_tradable=False)
        .first()
    )
    person = session.query(t.Person).filter_by(name="Доппио Дьяволо").first()
    (
        corsairs.append(
            t.Person_Item(
                person_id=person.id, save_id=SID, item_id=item.id, quantity=1
            )
        )
        if item and person
        else None
    )

    lst = civils + condots + corsairs

    args_handle(session, args, t.Person_Item, lst)
    if (args and not args.correct) or not args:
        session.add_all(lst)
    session.commit()


def fill_persons_weapons(session: Session, args) -> None:
    """Fill persons_weapons table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    civ_id : range
        The range of civilians id
    con_id : range
        The range of condottieri id
    cor_id : range
        The range of corsairs id
    args : Optional[Namespace]
        The command line argument
    """

    SID: int = 1
    persons = session.query(t.Person).filter_by(save_id=SID).all()
    lst = []
    for person in persons:
        weapons: Optional[List[t.Weapon]] = (
            session.query(t.Weapon).filter_by(name=person.weapon).all()
        )
        if weapons:
            find_weapon = [w for w in weapons if not w.is_tradable]
            lst.append(
                t.Person_Weapon(
                    person_id=person.id,
                    save_id=SID,
                    weapon_id=find_weapon[0].id,
                )
            )

    weapon = (
        session.query(t.Weapon)
        .filter_by(name="Парные пистоли", is_tradable=True)
        .first()
    )
    persons = [p for p in persons if p.name == "Леонардо Макаров"]
    lst += (
        [
            t.Person_Weapon(
                person_id=persons[0].id, save_id=SID, weapon_id=weapon.id
            )
        ]
        if weapon and persons
        else []
    )

    args_handle(session, args, t.Person_Weapon, lst)
    if (args and not args.correct) or not args:
        session.add_all(lst)
    session.commit()


def fill_quests(session: Session, args: Optional[Namespace]):
    """Fill quests table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line argument
    """

    quests: List[t.Quest] = []

    # Condottieri's quests
    CID: ClassID = ClassID.CONDOTR
    # 1
    brief: str = "Следы кота"
    text: str = (
        "Уже слышал, что пропал кот короля? Видишь следы вокруг? Проследи,"
        "может они приведут тебя к коту!"
    )
    kind: QuestKind = QuestKind.TRACE
    reward: int = 1000
    lid: int = 1
    item: str = "🐾"

    rec: Optional[t.Person] = (
        session.query(t.Person)
        .filter_by(name="Денис Риччи", save_id=1)
        .first()
    )
    if rec:
        condition: str = (
            f"npc.id == '{rec.id}' and '{brief}' in [q.brief for q in"
            " hero.questbook if not q.is_done]"
        )
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                location_id=lid,
                item=item,
                receiving_npc_id=rec.id,
                condition=condition,
                class_id=CID,
            )
        )

    # 2
    brief = "Письмо для сослуживца"
    text = (
        "Передай письмо моему товарищу в Трактире на пристани, и приходи"
        " обратно"
    )
    kind = QuestKind.DELIVERY
    reward = 1000
    item = "Письмо друга"
    start_condition: str = (
        "'Следы кота' in [q.brief for q in" " self.questbook if not q.is_done]"
    )

    reward_item: str = "Кортик"
    reward_item_quantity: int = 1
    rec = (
        session.query(t.Person)
        .filter_by(name="Франческо Тотти", save_id=1)
        .first()
    )
    if rec:
        condition = (
            f"npc.id == '{rec.id}' and '{brief}' in [q.brief for q in"
            f" hero.questbook if not q.is_done] and '{item}' in [i.name for i"
            " in hero.inventory]"
        )
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                item=item,
                start_condition=start_condition,
                condition=condition,
                receiving_npc_id=rec.id,
                class_id=CID,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    # 3
    brief = "Го"
    text = "Выиграй в го у Дениса Риччи"
    kind = QuestKind.GO
    reward = 1000
    item = "False"
    start_condition = (
        "'Письмо для сослуживца' in [q.brief for q in self.questbook"
        " if q.is_done]"
    )
    condition = (
        f"'{brief}' in [q.brief for q in hero.questbook if not q.is_done] and"
        f" [q for q in hero.questbook if q.brief == '{brief}'][0].item =="
        " 'True'"
    )
    quests.append(
        t.Quest(
            brief=brief,
            description=text,
            kind=kind,
            reward=reward,
            item=item,
            start_condition=start_condition,
            condition=condition,
            class_id=CID,
        )
    )

    # 4
    brief = "К озёрам"
    text = "Спроси кондотьера на западе про убегающего корсара"
    kind = QuestKind.FIND
    reward = 2000
    rec = (
        session.query(t.Person)
        .filter_by(name="Николай Сфорца", save_id=1)
        .first()
    )
    start_condition = (
        "'Го' in [q.brief for q in self.questbook" " if q.is_done]"
    )

    if rec:
        condition = (
            f"npc.id == '{rec.id}' and '{brief}' in [q.brief for q in"
            " hero.questbook if not q.is_done]"
        )
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                start_condition=start_condition,
                condition=condition,
                receiving_npc_id=rec.id,
                class_id=CID,
            )
        )

    # 5
    brief = "Разборка с корсаром"
    text = "Нужно разобраться с корсаром, есть подозрение, что кошка у него"
    kind = QuestKind.BATTLE
    reward = 2500
    start_condition = (
        "'Го' in [q.brief for q in self.questbook" " if q.is_done]"
    )

    rec = (
        session.query(t.Person)
        .filter_by(name="Самир Вендетта", save_id=1)
        .first()
    )
    if rec:
        condition = (
            f"enemy.name == '{rec.name}' and '{brief}' in [q.brief"
            " for q in self.questbook if not q.is_done]"
        )
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                start_condition=start_condition,
                condition=condition,
                receiving_npc_id=rec.id,
                class_id=CID,
            )
        )

    # 6
    brief = "Го"
    text = "Выиграй в го у Джанкарло Эспозито"
    kind = QuestKind.GO
    reward = 2500
    item = "False"
    start_condition = (
        "'Го' in [q.brief for q in self.questbook" " if q.is_done]"
    )
    condition = (
        f"'{text}' in [q.description for q in hero.questbook if not q.is_done]"
        " and [q for q in hero.questbook  if q.description =="
        f" '{text}'][0].item == 'True'"
    )
    quests.append(
        t.Quest(
            brief=brief,
            description=text,
            kind=kind,
            reward=reward,
            start_condition=start_condition,
            condition=condition,
            item=item,
            class_id=CID,
        )
    )

    # 7
    brief = "Откровение"
    text = "Я узнал, что Денис Риччи врал, и кошка у него"
    kind = QuestKind.FIND
    reward = 2500
    start_condition = (
        "'Выиграй в го у Джанкарло Эспозито' in [q.description for q in"
        " self.questbook if q.is_done]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Денис Риччи", save_id=1)
        .first()
    )
    if rec:
        condition = (
            f"npc.id == '{rec.id}' and '{brief}' in [q.brief for q in"
            " hero.questbook if not q.is_done]"
        )
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                start_condition=start_condition,
                condition=condition,
                receiving_npc_id=rec.id,
                class_id=CID,
            )
        )

    # 8
    brief = "Спасение кота"
    text = "Кота короля переворовали! Его нужно спасти из лап корсаров"
    kind = QuestKind.UNION_AND_GRAB
    reward = 3500
    item = "Кот короля"
    quantity: int = 1
    start_condition = (
        "'Откровение' in [q.brief for q in" " self.questbook if not q.is_done]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Доппио Дьяволо", save_id=1)
        .first()
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Доппио Дьяволо", save_id=1)
        .first()
    )
    if rec:
        condition = f"'{item}' in [i.name for i in hero.inventory]"
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                item=item,
                quantity=quantity,
                start_condition=start_condition,
                condition=condition,
                receiving_npc_id=rec.id,
                class_id=CID,
            )
        )

    # 9
    brief = "Задание короля"
    text = "Король дал задание, найти его кота. Зацепок нет"
    kind = QuestKind.UNION_AND_GRAB
    item = "Кот короля"
    quantity = 1
    start_condition = (
        "'Возвращение кота' not in [q.brief for q in" " self.questbook]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Доппио Дьяволо", save_id=1)
        .first()
    )
    if rec:
        condition = f"'{item}' in [i.name for i in hero.inventory]"
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                item=item,
                quantity=quantity,
                start_condition=start_condition,
                condition=condition,
                receiving_npc_id=rec.id,
                class_id=CID,
            )
        )

    # 10
    brief = "Возвращение кота"
    text = "Наконец вы нашли кота! Но хотите ли вы вернуть его королю?"
    kind = QuestKind.BATTLE_AND_DELIVERY
    reward = 5000
    reward_item = "Пиастра"
    reward_item_quantity = 1000
    item = "Кот короля"
    quantity = 1
    rec = (
        session.query(t.Person)
        .filter_by(name="Маттео Тапочкин", save_id=1)
        .first()
    )
    if rec:
        condition = (
            f"npc.id == '{rec.id}' and '{brief}' in [q.brief for q in"
            f" hero.questbook if not q.is_done] and '{item}' in [i.name for i"
            " in hero.inventory]"
        )
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                kind=kind,
                reward=reward,
                item=item,
                quantity=quantity,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
                condition=condition,
                receiving_npc_id=rec.id,
                class_id=CID,
            )
        )

    # corsairs quests
    # 1
    brief = "Подстава"
    text = "Найди Омара Капоне на западе в Ореховом лесу"
    rec = (
        session.query(t.Person)
        .filter_by(name="Омар Капоне", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Джованни Чичиков", save_id=1)
        .first()
    )
    if rec and giv:
        condition = f"npc.id == str({rec.id})"
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=1,
                kind=QuestKind.FIND,
                reward=1000,
                receiving_npc_id=rec.id,
                giving_npc_id=giv.id,
                condition=condition,
                class_id=ClassID.CORSAIR,
            )
        )
    # 2
    brief = "Тот самый.. Ризотто Неро"
    text = "Найди Ризотто Неро на юге в Коралловом гроте."
    start_condition = (
        "'Финальный бой' not in [q.brief for q in self.questbook] and"
        " 'Подстава' in [q.brief for q in self.questbook]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Ризотто Неро", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Омар Капоне", save_id=1)
        .first()
    )
    if rec and giv:
        condition = f"npc.id == str({rec.id})"
        reward_item = "Сабля"
        reward_item_quantity = 1
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=1,
                kind=QuestKind.FIND,
                reward=1000,
                receiving_npc_id=rec.id,
                giving_npc_id=giv.id,
                condition=condition,
                start_condition=start_condition,
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )
    # 3
    brief = "Бутылка вина"
    text = "Принеси вина для Ризотто."
    start_condition = (
        "'Сильнейший' not in [q.brief for q in self.questbook] and"
        " 'Бутылка вина' not in [item.name for item in self.inventory]"
        " and 'Тот самый.. Ризотто Неро' in [q.brief for q in self.questbook]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Джамал Корлеоне", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Ризотто Неро", save_id=1)
        .first()
    )
    if rec and giv:
        condition = f"npc.id == str({rec.id})"
        reward_item = "Стальной нагрудник"
        reward_item_quantity = 1
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=7,
                kind=QuestKind.FIND,
                reward=1000,
                receiving_npc_id=rec.id,
                giving_npc_id=giv.id,
                condition=condition,
                start_condition=start_condition,
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )
    # 4
    brief = "Испытание смелости"
    text = (
        "Одолей Северуса Снейпа и приходи к Месуту Озилу на юг на"
        " Банановый остров."
    )
    start_condition = (
        "'Сильнейший' not in [q.brief for q in self.questbook] and"
        " 'Тот самый.. Ризотто Неро' in [q.brief for q in self.questbook"
        " if q.is_done]")
    rec = (
        session.query(t.Person).filter_by(name="Месут Озил", save_id=1).first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Джамал Корлеоне", save_id=1)
        .first()
    )
    if rec and giv:
        condition = f"npc.id ==str({rec.id})"
        reward_item = "Бутылка вина"
        reward_item_quantity = 1
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=7,
                kind=QuestKind.FIND,
                reward=2500,
                receiving_npc_id=rec.id,
                giving_npc_id=rec.id,
                condition=condition,
                start_condition=start_condition,
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )
    # 5
    brief = "Сильнейший"
    text = "Держи бутылку вина и возвращайся к Ризотто"
    start_condition = (
        "'Бутылка вина' in [q.brief for q in self.questbook if q.is_done]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Ризотто Неро", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person).filter_by(name="Месут Озил", save_id=1).first()
    )
    if rec and giv:
        condition = f"npc.id ==str({rec.id})"
        item = "Бутылка вина"
        reward_item = "Пиво"
        reward_item_quantity = 2
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=5,
                kind=QuestKind.DELIVERY,
                item=item,
                reward=3000,
                receiving_npc_id=rec.id,
                giving_npc_id=rec.id,
                condition=condition,
                start_condition=start_condition,
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )
    # 6
    brief = "Подготовка"
    text = "Отправляйся к Джорно Джованне на восток в Базарные переулки"
    start_condition = (
        "'Бутылка вина' in [item.name for item in self.inventory]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Джорно Джованна", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Ризотто Неро", save_id=1)
        .first()
    )
    if rec and giv:
        condition = f"npc.id ==str({rec.id})"
        reward_item = "Мешок с мукой"
        reward_item_quantity = 1
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=10,
                kind=QuestKind.FIND,
                reward=1000,
                receiving_npc_id=rec.id,
                giving_npc_id=rec.id,
                start_condition=start_condition,
                condition=condition,
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    brief = "Финальный бой"
    text = (
        "Найди Винсента ван Гога на севере в Трактире на пристани и срази его."
        "\nПосле отправляйся к Омару Капоне в Ореховый лес."
    )
    start_condition = (
        "'Сильнейший' in [q.brief for q in self.questbook if q.is_done]"
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Омар Капоне", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Джорно Джованна", save_id=1)
        .first()
    )
    if rec and giv:
        condition = f"npc.id ==str({rec.id})"
        reward_item = "Удостоверение заслуженного корсара"
        reward_item_quantity = 1
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=2,
                kind=QuestKind.FIND,
                reward=5000,
                receiving_npc_id=rec.id,
                giving_npc_id=rec.id,
                condition=condition,
                start_condition=start_condition,
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    for q in quests:
        setattr(q, "is_done", False)

    args_handle(session, args, t.Quest, quests)
    if (args and not args.correct) or not args:
        session.add_all(quests)
    session.commit()


def fill_persons_quests(session: Session, args: Optional[Namespace]) -> None:
    """Fill persons quests table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    args : Optional[Namespace]
        The command line argument
    """

    SID: int = 1
    quests: Optional[List[t.Quest]] = session.query(t.Quest).all()
    if quests is None:
        raise ValueError("Quests table empty")
    persons_quests: List[t.Person_Quest] = []

    def add_person_quest(name, brief=None, description=None) -> None:
        npc: Optional[t.Person] = (
            session.query(t.Person).filter_by(name=name, save_id=SID).first()
        )
        quest: Optional[t.Quest] = None
        if brief:
            fit_quests = (
                [q for q in quests if q.brief == brief] if quests else []
            )
            quest = fit_quests[0] if fit_quests else None
        elif description:
            fit_quests = (
                [q for q in quests if q.description == description]
                if quests
                else []
            )
            quest = fit_quests[0] if fit_quests else None
        if npc and quest:
            quest.giving_npc_id = npc.id
            persons_quests.append(
                t.Person_Quest(
                    person_id=npc.id,
                    save_id=SID,
                    quest_id=quest.id,
                )
            )
        elif not quest:
            raise ValueError("Quest did not found")
        elif not npc:
            raise ValueError("NPC did not found")

    add_person_quest("Джованни Чичиков", "Следы кота")
    add_person_quest("Денис Риччи", "Письмо для сослуживца")
    add_person_quest("Денис Риччи", "Го")
    add_person_quest("Денис Риччи", "К озёрам")
    add_person_quest("Николай Сфорца", "Разборка с корсаром")
    add_person_quest(
        "Джанкарло Эспозито", description="Выиграй в го у Джанкарло Эспозито"
    )
    add_person_quest("Джанкарло Эспозито", "Откровение")
    add_person_quest("Денис Риччи", "Спасение кота")
    add_person_quest("Доппио Дьяволо", "Возвращение кота")
    add_person_quest("Маттео Тапочкин", "Задание короля")

    # for corsairs
    add_person_quest("Джованни Чичиков", "Подстава")
    add_person_quest("Омар Капоне", "Тот самый.. Ризотто Неро")
    add_person_quest("Ризотто Неро", "Бутылка вина")
    add_person_quest("Джамал Корлеоне", "Испытание смелости")
    add_person_quest("Месут Озил", "Сильнейший")
    add_person_quest("Ризотто Неро", "Подготовка")
    add_person_quest("Джорно Джованна", "Финальный бой")

    for pq in persons_quests:
        pq.is_done = False

    args_handle(session, args, t.Person_Quest, persons_quests)
    if (args and not args.correct) or not args:
        session.add_all(persons_quests)
    session.commit()
