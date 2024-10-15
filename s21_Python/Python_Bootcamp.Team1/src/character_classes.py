"""The script describes the game characters

Script requires annotations to annotate implicit NPC and ENEMY
classes in Protagonist methods, defaultdict - to implement inventory,
random - to imitate dice throw, tables - to fill weapon attribute
"""

from __future__ import annotations
from collections import defaultdict
import math
import random as r
import tables as t
import copy
from enum import IntEnum, Enum
from dataclasses import dataclass, field
from typing import Dict, List, Union, Any

INIT_HP: int = 10
LEVEL_EXP: int = 1000
DEFEAT: str = "Вы мертвы..."
ENEMY_DEFEAT: str = "Враг повержен"


class ClassID(IntEnum):
    """Class id enumerate"""

    CIVIL = 1
    CONDOTR = 2
    CORSAIR = 3


class QuestKind(IntEnum):
    """Quest kind enumerate"""

    TRACE = 1
    FIND = 2
    DELIVERY = 3
    TIC_TAC_TOE = 4


class Phrases(Enum):
    INIT = "Приветствую"
    END = "Бывай"
    WHATS_NEW = "Что нового?"
    QUEST_NEW = "Будет поручение?"
    ANGRY_END_CON = "Сдавайся!"
    ANGRY_END_COR = "Стой, ты, презренный пес!"
    END_CIV = "Иди с миром!"
    END_CON = "Будь здоров сослуживец!"
    END_COR = "Прощай, дружище!"
    ACCEPT_QUEST = "Я берусь за задание"
    REFUSE_QUEST = "Я не буду этого делать"
    GRATITUDE_CIV = "Спасибо за помощь!"
    GRATITUDE_CON = "Благодарю, Ваша светлость!"
    GRATITUDE_COR = "Спасибо, дружище!"
    UPSET_CIV = "Ну может в следующий раз"
    UPSET_CON = "Признаться, я ожидал более активных действий!"
    UPSET_COR = "Эх, ну ты даешь, друже!"
    LETS_PLAY = "Сыграем"


@dataclass
class Item:
    id: int = 0
    name: str = ""
    description: str = ""
    buff_parameter: int = 0
    buff: int = 0
    debuff: int = 0
    duration: int = 0
    cost: int = 0
    is_tradable: bool = False

    def __hash__(self):
        return hash((self.name, self.id))

    def __eq__(self, other):
        if not isinstance(other, Weapon):
            return NotImplemented
        return self.name == other.name and self.id == other.id


@dataclass
class Weapon:
    id: int = 0
    name: str = ""
    range: int = 0
    dmg_min: int = 0
    dmg_max: int = 0
    cost: int = 0
    is_tradable: bool = False

    def __hash__(self):
        return hash((self.name, self.id))

    def __eq__(self, other):
        if not isinstance(other, Weapon):
            return NotImplemented
        return self.name == other.name and self.id == other.id


@dataclass
class Quest:
    id: int = 0
    brief: str = ""
    description: str = ""
    reward: int = 0
    reward_item: str = ""
    reward_item_quantity: int = 0
    kind: int = 0
    condition: str = ""
    is_done: bool = False
    pos: List[int] = field(default_factory=list)
    item: str = ""
    quantity: int = 0
    location_id: int = 0
    giving_npc_id: str = ""
    receiving_npc_id: str = ""
    class_id: int = 0

    def __hash__(self):
        return hash((self.name, self.id))

    def __eq__(self, other):
        if not isinstance(other, Weapon):
            return NotImplemented
        return self.name == other.name and self.id == other.id


class Protagonist:
    """The character that the player controls

    Attributes
    ----------
    id : str
        The uud4 generated unique identificator
    name : str
        The character name
    class_id : int
        The character class identificator
    hp : int
        The health points of character
    weapon_damage : int
        The additional damage dealt by weapon
    weapon_range : int
        The range of weapon in hand
    level : int
        The level of character
    exp : int
        The experience required to control the level
    inventory : Dict[str, int]
        The inventory of character
    questbook : List[int] = list()
        The list of given quests
    __pos : Direction
        Current position of character
    """

    def __init__(self, name="Unknown", id="1", class_id=1) -> None:
        self.id: str = id
        self.name: str = name
        self.class_id: int = class_id
        self.hp: int = INIT_HP
        self.level: int = 1
        self.exp: int = 0
        self.inventory: Dict[Union[Item, Weapon], int] = defaultdict(int)
        self.questbook: List[t.Quest] = []
        self.location_id: int = 1
        self.__pos: Direction = Direction(0, 0)
        self.weapon: Weapon
        self.armor: Item
        self.pursuit_time: int = 0
        self.appearance: str = ""

    def talk_to(
        self, npc: Union[NPC, Enemy], msg: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """The dialogue with NPC

        Parameters
        ----------
        npc : NPC
            The character we are talking to
        """

        phrase: str = "..."
        responses: List[str] = ["Бывай"]
        msg_responses: List[Dict[str, Any]] = []
        phrases: Dict[str, Any] = data["phrases"]
        for key in phrases:
            if msg.startswith(key):
                msg_responses = phrases[key]
        if msg_responses:
            characters = data["characters"]
            response = self.__get_response(npc, characters, msg_responses)
            if response:
                phrase = response.get("text", "")
                responses = response.get("response", [""])
                if Phrases.ACCEPT_QUEST.value in responses:
                    idx: int = responses.index(Phrases.ACCEPT_QUEST.value)
                    if npc.questbook:
                        responses[idx] = (
                            Phrases.ACCEPT_QUEST.value
                            + ' "'
                            + npc.questbook[0].brief
                            + '"'
                        )
        if msg.startswith(Phrases.ACCEPT_QUEST.value):
            idx = msg.find('"') + 1
            brief: str = msg[idx:-1]
            found_quests = [q for q in npc.questbook if q.brief == brief]
            if found_quests:
                quest = found_quests[0]
                my_quest = copy.deepcopy(quest)
                self.questbook.append(my_quest)
                npc.questbook.remove(quest)
                if quest.kind == QuestKind.DELIVERY:
                    item = [i for i in data["items"] if i.name == quest.item][
                        0
                    ]
                    if item:
                        self.inventory[item] += 1
        return {"phrase": phrase, "responses": responses}

    def __get_response(
        self,
        npc: Union[NPC, Enemy],
        characters: Dict[str, Any],
        responses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """_summary_

        Parameters
        ----------
        npc : Union[NPC, Enemy]
            The person with whom the conversation takes place
        phrases : List[t.Phrase]
            The list of NPCs phrases

        Returns
        -------
        t.Phrase
            The current phrase
        """

        response = {}
        for dct in responses:
            condition = dct.get("condition", None)
            if condition is not None:
                eval_condition: bool = eval(condition)
                if eval_condition:
                    response = dct
                    break
            else:
                response = dct
        return response

    def attack(self, enemy: Enemy) -> str:
        """The battle with enemy

        Comparasion of dice value + weapon damage

        Parameters
        ----------
        enemy : Enemy
            The enemy we fight

        Returns
        -------
        str
            The result of attack
        """

        result: str = ""

        proto_damage: int = self.__get_damage(enemy)
        enemy_damage: int = enemy.__get_damage(self)

        if enemy.hp <= 0:
            result = "..."
        elif proto_damage == enemy_damage:
            result = r.choice(["Вы оба промахнулись!", "Вы оба увернулись"])
        else:
            try:
                enemy.take_hit(proto_damage)
                self.take_hit(enemy_damage)
                status: str = ""
                if enemy.hp > INIT_HP * (1 + enemy.level / 2) * 0.75:
                    status = "полно"
                elif enemy.hp > INIT_HP * (1 + enemy.level / 2) * 0.4:
                    status = "хватает"
                else:
                    status = "мало"
                result = self.__result_text(proto_damage, enemy_damage, status)
            except Exception as e:
                if self.hp > 0:
                    result = self.__enemy_defeat(enemy)
                else:
                    result = str(e)
        return result

    def __get_damage(self, enemy: Union[Protagonist, Enemy]) -> int:
        level_part: int = math.ceil(self.level / 6 * r.randint(1, 6))
        weapon_part: int = r.randint(self.weapon.dmg_min, self.weapon.dmg_max)
        armor_part: int = math.floor(enemy.armor.buff / 3 * r.randint(1, 3))
        result: int = level_part + weapon_part - armor_part
        return result if result > 0 else 0

    def __result_text(
        self, proto_damage: int, enemy_damage: int, status: str
    ) -> str:
        result: str = ""
        if proto_damage:
            result += "Враг теряет здоровье\n"
        else:
            result += "Враг не получает урона\n"
        result += f"У него {status} здоровья\n"
        if enemy_damage:
            result += "Вы теряете здоровье\n"
        else:
            result += "Вы не получаете урона\n"
        result += f"Ваше здоровье {self.hp}"
        return result

    def __enemy_defeat(self, enemy: Enemy):
        exp: int = int(LEVEL_EXP / 3 * enemy.level)
        self.advance_exp(exp)
        result = f"{ENEMY_DEFEAT}\nВы получили {exp} опыта"
        return result

    def take_hit(self, value=1):
        """Decrease healt point and die check

        Parameters
        ----------
        value : int, optional
            the strength of hit, by default 1

        Raises
        ------
        Exception
            Game Over exception
        """

        self.hp -= value
        if self.hp <= 0:
            raise Exception(DEFEAT)

    def heal(self, value=1):
        """Increase health points

        Parameters
        ----------
        value : int, optional
            The strength of heal, by default 1
        """

        self.hp += 1

    def advance_exp(self, value: int) -> str:
        """Increase experience level and check level up

        Parameters
        ----------
        value : int
            The experience value
        """

        result: str = f"Вы получили {value} опыта"
        self.exp += value
        threshold: int = self.level * 1000
        while self.exp >= threshold:
            result += "\n" + self.advance_level()
            self.exp -= threshold
        return result

    def advance_level(self, value: int = 1) -> str:
        """Increase level

        Parameters
        ----------
        value : int, optional
            The increase level, by default 1
        """

        self.level += value
        result: str = f"Теперь у Вас {self.level} уровень"
        self.hp = int(INIT_HP * (1 + self.level / 2))
        return result

    def go(self, direction: Direction):
        """Changes the position of character

        Parameters
        ----------
        direction : Direction
            New current position
        """

        self.__pos = direction

    def whereami(self) -> Direction:
        """Returns current position

        Returns
        -------
        Direction
            The current position
        """

        return self.__pos

    def set_pos(self, x, y):
        """Add new position

        Add
        -------
        Direction
            The new position
        """

        self.__pos = Direction(x, y)

    def take(self, item: Union[Item, Weapon], quantity=1) -> None:
        """Take the item

        Parameters
        ----------
        item : Union[Item, Weapon]
           Taken item
        """

        self.inventory[item] += quantity

    def throw(self, item: Union[Item, Weapon], quantity=1):
        self.inventory[item] -= quantity
        if self.inventory[item] == 0:
            del self.inventory[item]
        elif self.inventory[item] < 0:
            raise ValueError("Item quantity unavailable")

    def give(self, npc: NPC, item: Union[Item, Weapon], quantity=1):
        """Give the item

        Parameters
        ----------
        npc : NPC
            The receiving NPC
        item : Union[Item, Weapon]
            Given item
        """

        self.throw(item, quantity)
        npc.receive(item, quantity)

    def __quest_reward(self):
        # Пока не понятно как
        pass


class Direction:
    """Position on the map

    Attributes
    ----------
    x : int
        The x coordinate
    y : int
        The y coordinate
    """

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class NPC(Protagonist):
    """The non-playable character class"""

    def __init__(self, **kwargs) -> None:
        super().__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == "pos":
                    value = Direction(value[0], value[1])
                setattr(self, key, value)

    def receive(self, item: Union[Item, Weapon], quantity=1) -> None:
        """Takes item from character

        Parameters
        ----------
        item : Union[Item, Weapon]
            Taken item
        """

        self.take(item, quantity)

    def give(self, hero: Protagonist, item: Union[Item, Weapon], quant=1):
        if item is not None:
            self.inventory[item] -= quant
            if self.inventory[item] == 0:
                del self.inventory[item]
            elif self.inventory[item] < 0:
                raise ValueError("Item quantity unavailable")
            hero.take(item, quant)


class Enemy(NPC):
    """The enemy NPC class"""

    pass
