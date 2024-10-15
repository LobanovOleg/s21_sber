"""The script fill database tables

Script requires tables to link the specified data with ORM models,
Session - to add data to the correct PostgreSQL session, ClassId - to
select the correct class identifier, IntEnum - to create an enumeration
of class types
"""

import tables as t
from sqlalchemy.orm import Session  # type: ignore
from enum import IntEnum
from character_classes import INIT_HP, ClassID, QuestKind
from typing import List


class ItemBuff(IntEnum):
    """Item buff enumerate"""

    HP = 1
    DAMAGE = 2
    DEFENSE = 3


def fill_database(session: Session) -> None:
    """Fill databases with start values

    Parametersl
    ----------
    session : Session
        The PostgreSQL session
    """

    civils_id = range(1, 11)
    condattieri_id = range(11, 21)
    corsairs_id = range(21, 31)

    text: str = "Новая игра | SAVE ID 1"
    session.add(t.Save(id=1, description=text, time=0))
    fill_classes(session)
    fill_persons(session)
    fill_items(session)
    fill_weapons(session)
    fill_persons_items(session, civils_id, condattieri_id, corsairs_id)
    fill_persons_weapons(session, civils_id, condattieri_id, corsairs_id)
    quests: List[t.Quest] = fill_quests(session)
    fill_persons_quests(session, quests)


def fill_classes(session: Session) -> None:
    """Fill classes table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    """

    session.add_all(
        [
            t.Class(id=ClassID.CIVIL, name="Мирный житель"),
            t.Class(id=ClassID.CONDOTR, name="Кондотьер"),
            t.Class(id=ClassID.CORSAIR, name="Корсар"),
        ]
    )
    session.commit()


def fill_persons(session: Session) -> None:
    """Fill persons table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    """

    p: List[t.Person] = []
    SID: int = 1
    ID: int = 1

    def add_person(cid, ico, name, lvl, lid, pos):
        nonlocal ID
        person = t.Person(id=ID, class_id=cid, save_id=SID, appearance=ico)
        ID += 1
        person.name = name
        person.level = lvl
        person.location_id = lid
        person._Person__pos = pos
        person.hp = INIT_HP + person.level * 5
        p.append(person)

    def add_civ(name, lvl, lid, pos):
        ico = "🙎‍♂️"
        add_person(ClassID.CIVIL, ico, name, lvl, lid, pos)

    add_civ(name="Джованни Чичиков", lvl=1, lid=1, pos=[3, 3])
    add_civ(name="Альберто Синичкин", lvl=2, lid=2, pos=[12, 13])
    add_civ(name="Никколо Романов", lvl=3, lid=3, pos=[1, 3])
    add_civ(name="Массимо Иванов", lvl=4, lid=4, pos=[1, 21])
    add_civ(name="Джакомо Хаматдинов", lvl=4, lid=5, pos=[9, 4])
    add_civ(name="Леонардо Макаров", lvl=3, lid=6, pos=[13, 15])
    add_civ(name="Кристиан Харионов", lvl=4, lid=7, pos=[11, 3])
    add_civ(name="Франчексо Соболев", lvl=4, lid=8, pos=[5, 16])
    add_civ(name="Роберто Стечкин", lvl=4, lid=9, pos=[4, 3])
    add_civ(name="Маттео Тапочкин", lvl=4, lid=10, pos=[9, 1])
    add_civ(name="Джанкарло Эспозито", lvl=3, lid=11, pos=[15, 1])
    add_civ(name="Абригадо Тобакко", lvl=2, lid=12, pos=[19, 1])
    add_civ(name="Альфредо ди Стефано", lvl=1, lid=13, pos=[4, 3])
    add_civ(name="Дидье Дешам", lvl=4, lid=1, pos=[14, 5])
    add_civ(name="Андреа Пирло", lvl=1, lid=2, pos=[4, 0])
    add_civ(name="Антонио Маргаретти", lvl=1, lid=3, pos=[6, 5])
    add_civ(name="Доминик де Кокко", lvl=1, lid=4, pos=[7, 4])
    add_civ(name="Франческо Горломи", lvl=2, lid=5, pos=[17, 0])
    add_civ(name="Кристофф Вальц", lvl=2, lid=6, pos=[16, 0])
    add_civ(name="Матео Ковачич", lvl=1, lid=7, pos=[8, 1])
    add_civ(name="Олегос Лобановски", lvl=1, lid=8, pos=[8, 1])

    def add_con(name, lvl, lid, pos):
        ico = "💂🏼"
        add_person(ClassID.CONDOTR, ico, name, lvl, lid, pos)

    add_con(name="Иван Медичи", lvl=1, lid=9, pos=[1, 5])
    add_con(name="Руслан да Сан Северино", lvl=2, lid=10, pos=[1, 11])
    add_con(name="Николай Сфорца", lvl=2, lid=11, pos=[5, 7])
    add_con(name="Олег Пальмери", lvl=4, lid=12, pos=[5, 8])
    add_con(name="Владимир Мартини", lvl=4, lid=13, pos=[12, 5])
    add_con(name="Ильнур Коста", lvl=3, lid=1, pos=[13, 13])
    add_con(name="Денис Риччи", lvl=3, lid=1, pos=[14, 6])
    add_con(name="Александр Росси", lvl=2, lid=3, pos=[2, 7])
    add_con(name="Федор Фабрици", lvl=4, lid=4, pos=[9, 9])
    add_con(name="Леонид Луккези", lvl=4, lid=5, pos=[11, 15])
    add_con(name="Соске Айдзен", lvl=4, lid=6, pos=[16, 5])
    add_con(name="Северус Снейп", lvl=3, lid=7, pos=[19, 1])
    add_con(name="Марко Ройс", lvl=2, lid=8, pos=[8, 8])
    add_con(name="Джанлуиджи Буффон", lvl=2, lid=9, pos=[12, 7])
    add_con(name="Маскарпоне Палаццо", lvl=4, lid=10, pos=[16, 1])
    add_con(name="Массимилиано Аллегри", lvl=1, lid=11, pos=[2, 2])
    add_con(name="Клаудио Раньери", lvl=1, lid=12, pos=[3, 3])
    add_con(name="Кенпачи Дзараки", lvl=3, lid=13, pos=[9, 20])
    add_con(name="Франческо Тотти", lvl=2, lid=1, pos=[0, 7])
    add_con(name="Винсент ван Гог", lvl=4, lid=2, pos=[15, 4])
    add_con(name="Евпатий Коловрат", lvl=4, lid=3, pos=[7, 13])
    add_con(name="Яромир Мендельсон", lvl=2, lid=4, pos=[0, 15])

    def add_cor(name, lvl, lid, pos):
        ico = "👳🏼‍♂️"
        add_person(ClassID.CORSAIR, ico, name, lvl, lid, pos)

    add_cor(name="Али Клайд", lvl=2, lid=5, pos=[1, 6])
    add_cor(name="Салим Воробей", lvl=2, lid=6, pos=[2, 9])
    add_cor(name="Джамал Корлеоне", lvl=2, lid=7, pos=[7, 7])
    add_cor(name="Мустафа Романо", lvl=3, lid=8, pos=[16, 3])
    add_cor(name="Карим Кастилия", lvl=3, lid=9, pos=[12, 12])
    add_cor(name="Ашраф Леони", lvl=3, lid=10, pos=[12, 3])
    add_cor(name="Самир Вендетта", lvl=4, lid=11, pos=[12, 4])
    add_cor(name="Омар Капоне", lvl=3, lid=12, pos=[6, 16])
    add_cor(name="Сулейман Линч", lvl=2, lid=13, pos=[5, 15])
    add_cor(name="Ахмед Флойд", lvl=3, lid=1, pos=[0, 14])
    add_cor(name="Иван Медичи", lvl=4, lid=2, pos=[17, 20])
    add_cor(name="Жозе Моуриньо", lvl=2, lid=3, pos=[14, 10])
    add_cor(name="Генрих V", lvl=4, lid=4, pos=[15, 13])
    add_cor(name="Месут Озил", lvl=1, lid=5, pos=[0, 3])
    add_cor(name="Мартин Лютер", lvl=1, lid=6, pos=[8, 2])
    add_cor(name="Ризотто Неро", lvl=4, lid=7, pos=[13, 13])
    add_cor(name="Гвидо Миста", lvl=3, lid=8, pos=[16, 11])
    add_cor(name="Доппио Дьяволо", lvl=4, lid=9, pos=[18, 21])
    add_cor(name="Джорно Джованна", lvl=1, lid=10, pos=[2, 2])
    add_cor(name="Жан Пьер", lvl=1, lid=11, pos=[7, 3])
    add_cor(name="Ибрагим Паша", lvl=3, lid=12, pos=[6, 20])
    add_cor(name="Майк Тайсон", lvl=4, lid=13, pos=[14, 16])
    add_cor(name="Хобутус Плутович", lvl=1, lid=1, pos=[17, 21])

    for person in p:
        setattr(person, "is_protagonist", False)
    session.add_all(p)
    session.commit()


def fill_items(session: Session) -> None:
    """Fill items table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
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
    items.append(
        t.Item(
            name="Голое тело",
            buff_parameter=bp,
            buff=0,
            description="Без одежды",
            is_tradable=False,
        )
    )

    items.append(
        t.Item(
            name="Кожаный камзол",
            buff_parameter=bp,
            buff=5,
            description="Одежда корсара",
            is_tradable=False,
        )
    )
    items.append(
        t.Item(
            name="Кожаный камзол",
            buff_parameter=bp,
            buff=5,
            description="Одежда корсара",
            is_tradable=True,
            cost=50,
        )
    )

    items.append(
        t.Item(
            name="Стальной нагрудник",
            is_tradable=False,
            buff_parameter=bp,
            buff=10,
            description="Защита кондотьера",
        )
    )
    items.append(
        t.Item(
            name="Стальной нагрудник",
            is_tradable=True,
            buff_parameter=bp,
            buff=10,
            description="Защита кондотьера",
            cost=70,
        )
    )

    items.append(
        t.Item(
            name="Льняная рубашка",
            is_tradable=False,
            buff_parameter=bp,
            buff=1,
            description="Простая одежда",
        )
    )
    items.append(
        t.Item(
            name="Льняная рубашка",
            is_tradable=True,
            buff_parameter=bp,
            buff=1,
            description="Простая одежда",
            cost=20,
        )
    )

    # food
    items.append(
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
    items.append(
        t.Item(
            name="Вино",
            buff_parameter=ItemBuff.HP,
            buff=1,
            description="Любимый напиток жителя",
            duration=5,
            is_tradable=True,
            cost=3,
        )
    )
    items.append(
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
    items.append(
        t.Item(
            name="Вяленое мясо",
            buff_parameter=ItemBuff.HP,
            buff=5,
            is_tradable=True,
            cost=4,
            description="Питательная пища",
        )
    )
    items.append(
        t.Item(
            name="Галеты",
            buff_parameter=ItemBuff.HP,
            buff=3,
            description="Питательная пища",
            is_tradable=True,
            cost=2,
        )
    )
    items.append(
        t.Item(
            name="Жареная рыба",
            buff_parameter=ItemBuff.HP,
            buff=4,
            is_tradable=True,
            cost=3,
            description="Питательная пища",
        )
    )

    # special
    items.append(t.Item(name="Карта с кладом", is_tradable=False))
    items.append(
        t.Item(
            name="Удостоверение",
            buff_parameter=ItemBuff.DAMAGE,
            buff=1,
            description="Удостоверение кондотьера",
            is_tradable=False,
        )
    )

    # quest
    items.append(t.Item(name="Письмо друга", is_tradable=True))
    items.append(t.Item(name="Бутылка вина", is_tradable=True))
    items.append(t.Item(name="Удостоверение заслуженного корсара", is_tradable=False))
    session.add_all(items)
    session.commit()


def fill_weapons(session: Session) -> None:
    """Fill weapons table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
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
    session.add_all(weapons)
    session.commit()


def fill_persons_items(session: Session, civ_id, con_id, cor_id) -> None:
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

    session.add_all(civils + condots + corsairs)
    session.commit()


def fill_persons_weapons(session: Session, civ_id, con_id, cor_id) -> None:
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
    """

    SID: int = 1
    fists = session.query(t.Weapon).filter_by(name="Кулаки").first()
    civils = (
        [
            t.Person_Weapon(person_id=str(i), save_id=SID, weapon_id=fists.id)
            for i in civ_id
        ]
        if fists
        else []
    )
    weapon = (
        session.query(t.Weapon)
        .filter_by(name="Кортик", is_tradable=False)
        .first()
    )
    if weapon:
        civils += [
            t.Person_Weapon(person_id="1", save_id=SID, weapon_id=weapon.id)
        ]
        civils += [
            t.Person_Weapon(person_id="2", save_id=SID, weapon_id=weapon.id)
        ]
    weapon = (
        session.query(t.Weapon)
        .filter_by(name="Парные пистоли", is_tradable=True)
        .first()
    )
    civils += (
        [t.Person_Weapon(person_id="1", save_id=SID, weapon_id=weapon.id)]
        if weapon
        else []
    )

    weapon = (
        session.query(t.Weapon)
        .filter_by(name="Сабля", is_tradable=False)
        .first()
    )
    condots = (
        [
            t.Person_Weapon(person_id=str(i), save_id=SID, weapon_id=weapon.id)
            for i in con_id
        ]
        if weapon
        else []
    )
    weapon = (
        session.query(t.Weapon)
        .filter_by(name="Ружье", is_tradable=False)
        .first()
    )
    condots += (
        [t.Person_Weapon(person_id="20", save_id=SID, weapon_id=weapon.id)]
        if weapon
        else []
    )

    weapon = (
        session.query(t.Weapon)
        .filter_by(name="Топор", is_tradable=False)
        .first()
    )
    corsairs = (
        [
            t.Person_Weapon(person_id=str(i), save_id=SID, weapon_id=weapon.id)
            for i in cor_id
        ]
        if weapon
        else []
    )
    weapon = (
        session.query(t.Weapon)
        .filter_by(name="Парные пистоли", is_tradable=False)
        .first()
    )
    condots += (
        [t.Person_Weapon(person_id="30", save_id=SID, weapon_id=weapon.id)]
        if weapon
        else []
    )
    session.add_all(civils + condots + corsairs)
    session.commit()


def fill_quests(session: Session) -> List[t.Quest]:
    """Fill quests table

    Parameters
    ----------
    session : Session
        The PostgreSQL session
    """

    quests: List[t.Quest] = []

    brief: str = "Следы кота"
    text: str = "Видишь следы вокруг? Проследи, может это приведет тебя к коту"
    rec = (
        session.query(t.Person)
        .filter_by(name="Денис Риччи", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Джованни Чичиков", save_id=1)
        .first()
    )
    if rec and giv:
        condition: str = f"npc.id == str({rec.id})"
        item: str = "🐾"
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=1,
                kind=QuestKind.TRACE,
                reward=1000,
                item=item,
                receiving_npc_id=rec.id,
                giving_npc_id=giv.id,
                condition=condition,
                class_id=ClassID.CONDOTR,
            )
        )

    brief = "Письмо для сослуживца"
    text = "Передай письмо моему товарищу, и приходи обратно"
    rec = (
        session.query(t.Person)
        .filter_by(name="Франческо Тотти", save_id=1)
        .first()
    )
    giv = (
        session.query(t.Person)
        .filter_by(name="Денис Риччи", save_id=1)
        .first()
    )
    item = "Письмо друга"
    if rec and giv:
        condition = f"npc.id == str({rec.id})"
        reward_item: str = "Кортик"
        reward_item_quantity: int = 1
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                item=item,
                condition=condition,
                reward=1000,
                location_id=1,
                receiving_npc_id=rec.id,
                giving_npc_id=giv.id,
                kind=QuestKind.DELIVERY,
                class_id=ClassID.CONDOTR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    brief = "Крестики-нолики"
    text = "Выиграй в крестики-нолики у Дениса Риччи"
    giv = (
        session.query(t.Person)
        .filter_by(name="Денис Риччи", save_id=1)
        .first()
    )
    item = "False"
    if giv:
        condition = (
            f"npc.id == {giv.id} and {brief} in [q.brief for q in"
            " self.questbook] and [q for q in self.questbook if q.brief =="
            f" {brief}][0].item == 'True'"
        )
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                condition=condition,
                item=item,
                reward=1000,
                location_id=1,
                giving_npc_id=giv.id,
                kind=QuestKind.TIC_TAC_TOE,
                class_id=ClassID.CONDOTR,
            )
        )

    brief = "Подстава"
    text = "Найди Омара Капоне во второй западной локации."
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

    brief = "Тот самый.. Ризотто Неро"
    text = "Найди Ризотто Неро в третьей южной локации локации."
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

    brief = "Бутылка вина"
    text = "Принеси вина для Ризотто."
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
                class_id=ClassID.CORSAIR,
            )
        )

    brief = "Испытание смелости"
    text = (
        "Одолей Северуса Снейпа и приходи к Месуту Озилу в первую южную"
        " локацию."
    )
    rec = (
        session.query(t.Person)
        .filter_by(name="Северус Снейп", save_id=1)
        .first()
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
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    brief = "Сильнейший"
    text = "Держи бутлку вина и возвращайся к Ризотто"
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
        reward_item = "Сабля"
        reward_item_quantity = 1
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
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    brief = "Подготовка"
    text = "Отправляйся к Джорно Джованне в третью восточную локацию"
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
        reward_item = "Стальной нагрудник"
        reward_item_quantity = 1
        quests.append(
            t.Quest(
                brief=brief,
                description=text,
                location_id=10,
                kind=QuestKind.FIND,
                item=item,
                reward=1000,
                receiving_npc_id=rec.id,
                giving_npc_id=rec.id,
                condition=condition,
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    brief = "Финальный бой"
    text = ("Найди Винсента ван Гога в первой локации севера и срази его.\n"
            "После отправляйся к Омару Капоене во вторую западную локацию.")
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
                class_id=ClassID.CORSAIR,
                reward_item=reward_item,
                reward_item_quantity=reward_item_quantity,
            )
        )

    for q in quests:
        setattr(q, "is_done", False)
    session.add_all(quests)
    session.commit()
    return quests


def fill_persons_quests(session: Session, quests: List[t.Quest]) -> None:
    SID: int = 1
    persons_quests: List[t.Person_Quest] = []
    npc = (
        session.query(t.Person)
        .filter_by(name="Джованни Чичиков", save_id=1)
        .first()
    )
    brief: str = "Следы кота"
    (
        persons_quests.append(
            t.Person_Quest(
                person_id=npc.id,
                save_id=SID,
                quest_id=[q.id for q in quests if q.brief == brief][0],
            )
        )
        if npc
        else None
    )

    npc = (
        session.query(t.Person)
        .filter_by(name="Денис Риччи", save_id=1)
        .first()
    )
    brief = "Письмо для сослуживца"
    persons_quests.append(
        t.Person_Quest(
            person_id=npc.id,
            save_id=SID,
            quest_id=[q.id for q in quests if q.brief == brief][0],
        )
    ) if npc else None

    brief = "Крестики-нолики"
    persons_quests.append(
        t.Person_Quest(
            person_id=npc.id,
            save_id=SID,
            quest_id=[q.id for q in quests if q.brief == brief][0],
        )
    ) if npc else None

    npc = (
        session.query(t.Person)
        .filter_by(name="Джованни Чичиков", save_id=1)
        .first()
    )

    brief = "Подстава"
    (
        persons_quests.append(
            t.Person_Quest(
                person_id=npc.id,
                save_id=SID,
                quest_id=[q.id for q in quests if q.brief == brief][0],
            )
        )
        if npc
        else None
    )

    npc = (
        session.query(t.Person)
        .filter_by(name="Омар Капоне", save_id=1)
        .first()
    )
    brief = "Тот самый.. Ризотто Неро"
    (
        persons_quests.append(
            t.Person_Quest(
                person_id=npc.id,
                save_id=SID,
                quest_id=[q.id for q in quests if q.brief == brief][0],
            )
        )
        if npc
        else None
    )

    npc = (
        session.query(t.Person)
        .filter_by(name="Ризотто Неро", save_id=1)
        .first()
    )
    brief = "Бутылка вина"
    (
        persons_quests.append(
            t.Person_Quest(
                person_id=npc.id,
                save_id=SID,
                quest_id=[q.id for q in quests if q.brief == brief][0],
            )
        )
        if npc
        else None
    )

    npc = (
        session.query(t.Person)
        .filter_by(name="Джамал Корлеоне", save_id=1)
        .first()
    )

    brief = "Испытание смелости"
    (
        persons_quests.append(
            t.Person_Quest(
                person_id=npc.id,
                save_id=SID,
                quest_id=[q.id for q in quests if q.brief == brief][0],
            )
        )
        if npc
        else None
    )

    npc = (
        session.query(t.Person)
        .filter_by(name="Месут Озил", save_id=1)
        .first()
    )
    brief = "Сильнейший"
    persons_quests.append(
        t.Person_Quest(
            person_id=npc.id,
            save_id=SID,
            quest_id=[q.id for q in quests if q.brief == brief][0],
        )
    ) if npc else None

    npc = (
        session.query(t.Person)
        .filter_by(name="Ризотто Неро", save_id=1)
        .first()
    )
    brief = "Подготовка"
    persons_quests.append(
        t.Person_Quest(
            person_id=npc.id,
            save_id=SID,
            quest_id=[q.id for q in quests if q.brief == brief][0],
        )
    ) if npc else None

    npc = (
        session.query(t.Person)
        .filter_by(name="Джорно Джованна", save_id=1)
        .first()
    )
    brief = "Финальный бой"
    persons_quests.append(
        t.Person_Quest(
            person_id=npc.id,
            save_id=SID,
            quest_id=[q.id for q in quests if q.brief == brief][0],
        )
    ) if npc else None

    for pq in persons_quests:
        pq.is_done = False
    session.add_all(persons_quests)
    session.commit()
