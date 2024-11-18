"""The script describes the game characters and helper classes

Script presents the game class - Protagonist and the classes for
non-player characters - NPCs, also for convenience, the class - Enemy
was added. At the same time, non-player classes are inherited from the
game class. The script also provides separate classes for items,
weapons and quests loaded via the database.

Script requires annotations to annotate implicit NPC and ENEMY
classes in Protagonist methods, defaultdict - to implement inventory,
deque - to speed up the calculation of the minimum distance between
cells, math - to round values, random - to imitate dice throw, copy -
to makes deepcopy of items that belongs different persons, logging -
shows mistakes, enum - to creates enumerates, dataclasses - to create
dataclasses
"""

from __future__ import annotations
from collections import defaultdict, deque
import math
import random as r
import copy
import logging
from enum import IntEnum, Enum
from dataclasses import dataclass, field
from typing import Dict, List, Union, Any, Optional, Tuple, Iterator, Type

INIT_HP: int = 10
LEVEL_EXP: int = 1000


class ClassID(IntEnum):
    """Enumeration of class IDs in the game"""
    CIVIL = 1
    CONDOTR = 2
    CORSAIR = 3


PLAYABLE_CLS: Dict[str, ClassID] = {
    "Кондотьер ⚔️": ClassID.CONDOTR,
    "Корсар ☠️": ClassID.CORSAIR,
}


class QuestKind(IntEnum):
    """Enumeration of quest types"""
    TRACE = 1
    FIND = 2
    DELIVERY = 3
    GO = 4
    BATTLE = 5
    UNION = 6
    BATTLE_AND_DELIVERY = 7
    UNION_AND_GRAB = 8
    FIND_AND_GRAB = 9


class Phrases(Enum):
    """Enumeration the main phrases used in conversation"""
    INIT = "Приветствую"
    END = "Бывай"
    WHATS_NEW = "Что нового?"
    QUEST_NEW = "Будет поручение?"
    WHATS_QUEST = "Говори"
    ANGRY_END_CON = "Сдавайся!"
    ANGRY_END_COR = "Стой, ты, презренный пес!"
    END_CIV = "Иди с миром!"
    END_CON = "Будь здоров, сослуживец!"
    END_COR = "Прощай, дружище!"
    ACCEPT_QUEST = "Я берусь за задание"
    REFUSE_QUEST = "Я не буду этого делать"
    GRATITUDE_CIV = "Спасибо за помощь!"
    GRATITUDE_CON = "Благодарю, Ваша светлость!"
    GRATITUDE_COR = "Спасибо, дружище!"
    UPSET_CIV = "Ну может в следующий раз"
    UPSET_CON = "Признаться, я ожидал более активных действий!"
    UPSET_COR = "Эх, ну ты даешь, друже!"
    LETS_PLAY = "Давай сыграем"
    WIN = "Вы победили"
    WIN_REACT = "Хорошо играешь!"
    DEFEAT = "Вы мертвы..."
    ENEMY_DEFEAT = "повержен"
    BREAK_UNION = "Разорвать отряд с"
    NOTHING = "Ничего"


class Position(IntEnum):
    """Enumeration to check the correctness of the position"""
    CORRECT = 1
    OUT_FIELD = 2
    OBSTACLE = 3


class ItemBuff(IntEnum):
    """Enumeration displaying parameters that can be enhanced"""
    HP = 1
    DAMAGE = 2
    DEFENSE = 3


class MiniGames(Enum):
    """Mini games you can play with the characters"""
    GO = "Го"


class EndTypes(IntEnum):
    """Mini-game completion statuses"""
    NOT_END = 0
    HERO_WIN = 1
    NPC_WIN = 2
    DRAW = 3


@dataclass
class Item:
    """The items belongs to NPCs

    Attributes
    ----------
    id : int
        The item's ID
    name : str
        The item's name
    is_tradable : bool
        Item availability status for sale
    is_usable : bool
        Item availability status for using
    cost : int
        Optional item's cost
    description : str
        Optional description of the item
    buff_parameter : int
        Optional property of an item that allows the user of the item
    boof_reusable : bool
        If true item adds boost every turn
    to gain a boost to a game parameter
    buff : int
        Optional gain value
    debuff : int
        Optional attenuation value
    duration : int
        Optional duration of the item
    """

    id: int = 0
    name: str = ""
    is_tradable: bool = False
    is_usable: bool = False
    is_armor: bool = False
    description: str = ""
    buff_parameter: int = 0
    buff_reusable: bool = False
    buff: int = 0
    debuff: int = 0
    duration: int = 0
    cost: int = 0

    def __hash__(self):
        return hash((self.name, self.id))

    def __eq__(self, other):
        if not isinstance(other, Weapon):
            return NotImplemented
        return self.name == other.name and self.id == other.id


@dataclass
class Weapon:
    """The weapons belongs to NPCs

    Attributes
    ----------
    id : int
        The weapon's ID
    name : str
        The weapon's name
    is_tradable : bool
        Weapon availability status for sale
    cost : int
        Optional weapon's cost
    range : int
        Shows from what distance you can start an attack
    dmg_min : int
        The minimum damage a weapon can cause
    dmg_max : int
        The maximum damage a weapon can cause
    """

    id: int = 0
    name: str = ""
    is_tradable: bool = False
    cost: int = 0
    range: int = 0
    dmg_min: int = 0
    dmg_max: int = 0

    def __hash__(self):
        return hash((self.name, self.id))

    def __eq__(self, other):
        if not isinstance(other, Weapon):
            return NotImplemented
        return self.name == other.name and self.id == other.id


@dataclass
class Quest:
    """The quests belongs by NPCs

    Attributes
    ----------
    id : int
        The quest's ID
    brief : str
        The quest name
    description : str
        Description of the quest task
    kind : QuestKind
        Type of quest being performed
    condition : str
        Quest completion condition
    is_done : bool
        Quest completion status
    reward : int
        Amount of experience for successfully completing a quest
    reward_item : int
        Optional item for successfully completing the quest
    reward_item_quantity : int
        Optional item amount for successful completion of the quest
    start_condition : str
        Optional condition for receiving the quest
    pos : List[int]
        Optional position on location
    item : str
        Optional quest storage item
    quantity : int
        Optional quest storage item amount
    location_id : int
        Optional location ID
    giving_npc_id : str
        Optional ID of the NPC that gives the quest
    receiving_npc_id : str
        Optional ID of the NPC the quest is aimed at
    class_id: ClassID
        Optional ID that restricts other classes from giving quest
    """

    id: int = 0
    brief: str = ""
    description: str = ""
    kind: QuestKind = QuestKind.FIND
    condition: str = ""
    is_done: bool = False
    class_id: ClassID = ClassID.CIVIL
    reward: int = 0
    reward_item: str = ""
    reward_item_quantity: int = 0
    start_condition: str = ""
    pos: List[int] = field(default_factory=list)
    item: str = ""
    quantity: int = 0
    location_id: int = 0
    giving_npc_id: str = ""
    receiving_npc_id: str = ""

    def __hash__(self):
        return hash((self.brief, self.id))

    def __eq__(self, other):
        if not isinstance(other, Weapon):
            return NotImplemented
        return self.brief == other.name and self.id == other.id


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
    level : int
        The level of character
    exp : int
        The experience required to control the level
    inventory : Dict[str, int]
        The inventory of character
    questbook : List[int]
        The list of given quests
    location_id : int
        The current game field matrix
    __pos : Direction
        Current position of character
    weapon : Weapon
        The weapon in hand
    armor : Item
        Equipped armor
    pursuit_time : int
        Pursuit time in moves
    appearance: str
        Character icon
    """

    def __init__(self, name="Unknown", id="1", class_id=ClassID.CIVIL) -> None:
        """The game's protagonist initialization

        Parameters
        ----------
        name : str, optional
            The protagonist's name, by default Unknown
        id : str, optional
            The protagonist's ID, by default 1
        class_id : ClassID, optional
            The protagonist's class ID, by default ClassID.CIVIL
        """

        self.id: str = id
        self.name: str = name
        self.class_id: int = class_id
        self.hp: int = INIT_HP
        self.level: int = 1
        self.exp: int = 0
        self.inventory: Dict[Union[Item, Weapon], int] = defaultdict(int)
        self.questbook: List[Quest] = []
        self.location_id: int = 1
        self.__pos: Direction = Direction(0, 0)
        self.weapon: Weapon = Weapon()
        self.armor: Item = Item()
        self.pursuit_time: int = 0
        self.appearance: str = ""

    def talk_to(
        self, npc: Union[NPC, Enemy], msg: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """The dialogue with NPC

        Parameters
        ----------
        npc : Union[NPC, Enemy]
            The character we are talking to
        msg : str
            A text to be answered
        data : Dict[str, Any]
            Data loaded from db

        Returns
        -------
        Dict[str, Any]
           The replica and list of possible responses to this replica
        """

        text: str = "..."
        response: List[str] = [Phrases.END.value]
        text_response_lst: List[Dict[str, Any]] = []
        phrases: Dict[str, Any] = data["phrases"]
        for key in phrases:
            if msg.startswith(key):
                text_response_lst = copy.deepcopy(phrases[key])
        if text_response_lst:
            characters = data["npcs"] + data["enemies"]
            text_response = self.__get_response(
                npc, characters, msg, text_response_lst
            )
            if text_response:
                text = text_response.get("text", "")
                if text == Phrases.NOTHING.value:
                    text = self.__get_fresh_news(data)
                response = text_response.get("response", [""])
                self.__add_quest_name(npc, response)
        if msg.startswith(Phrases.ACCEPT_QUEST.value) or msg.startswith(
            Phrases.LETS_PLAY.value
        ):
            start_quest_name: str = '"'
            idx = msg.find(start_quest_name) + 1
            brief: str = msg[idx:-1]
            quest: Optional[Quest] = None
            for q in npc.questbook:
                if q.brief == brief and not q.is_done:
                    quest = q
                    break
            if quest:
                text, response = self.__quest_append(
                    npc, quest, data, text, response
                )
        return {"text": text, "response": response}

    def __get_response(
        self,
        npc: Union[NPC, Enemy],
        characters: Dict[str, Any],
        msg: str,
        text_response_lst: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Gives a new replica for the incoming text and replies to it

        Parameters
        ----------
        npc : Union[NPC, Enemy]
            The person with whom the conversation takes place
        characters : Dict[str, Any]
            Needed to check eval conditions person
        msg : str
            A text to be answered
        text_response_lst : List[Dict[str, Any]]
            The list of replicas and their possible responses

        Returns
        -------
        Dict[str, Any]
            The replica and list of possible responses to this replica

        """

        def get_dict(dct: Dict[str, Any]) -> Dict[str, Any]:
            """Gets quest's text, responses pair

            Parameters
            ----------
            dct : Dict[str, str]
                The pair beind tested

            Returns
            -------
            Dict[str, str]
                Checked quest's text, responses pair
            """

            text_response = dct
            if msg == Phrases.WHATS_QUEST.value or msg.startswith(
                    Phrases.ACCEPT_QUEST.value):  # dynamic description
                try:
                    text_response["text"] = self.__is_condition(
                        npc, text_response, "text"
                    )
                except ValueError:
                    pass
                finally:
                    quests = [q for q in npc.questbook if not q.is_done]
                    quest = quests[0] if quests else None
                    if quest and hasattr(quest, "start_condition"):
                        if quest.start_condition and not eval(
                            quest.start_condition
                        ):
                            text_response["text"] = "Ничего нет"
                            text_response["response"] = [
                                Phrases.WHATS_NEW.value,
                                Phrases.END.value,
                            ]

            return text_response

        text_response = {}
        for dct in text_response_lst:
            is_end: bool = False
            condition = dct.get("condition", None)
            if condition is None:
                text_response = dct
                is_end = True
            else:
                eval_condition = self.__is_condition(npc, dct, "condition")
                if eval_condition:
                    text_response = get_dict(dct)
                    is_end = True
            if is_end:
                break
        return text_response

    def __is_condition(
        self, npc: Union[NPC, Enemy], dct: Dict[str, Any], condition: str
    ) -> Any:
        """Returns the condition of the replica if it exists

        Parameters
        ----------
        npc : Union[NPC, Enemy]
            Needed to check eval conditions person
        dct : Dict[str, Any]
            The replica and list of possible responses dictionary
        condition : str
            Condition to be checked

        Returns
        -------
        Any
            Returns evaluated text or bool value if condition exists

        Raises
        ------
        BaseException
            If eval incorrect
        """

        condition = dct.get(condition, None)
        if condition is not None:
            try:
                return eval(condition)
            except BaseException:
                raise ValueError("eval incorrect")

    def __add_quest_name(self, npc: NPC, response: List[str]) -> None:
        """Adds a quest brief to replica if replica is accepting quest

        Parameters
        ----------
        npc : NPC
            To check the quests completion status

        response : List[str]
            The list of replicas resonses
        """

        acpt: str = Phrases.ACCEPT_QUEST.value
        play: str = Phrases.LETS_PLAY.value
        res: str = ""
        idx: int = -1
        if acpt in response:
            idx = response.index(acpt)
            res = acpt
        elif play in response:
            idx = response.index(play)
            res = play
        if idx != -1:
            is_ok: bool = True
            new_quests = [q for q in npc.questbook if not q.is_done]
            if new_quests and hasattr(new_quests[0], "start_condition"):
                if new_quests[0].start_condition and not eval(
                    new_quests[0].start_condition
                ):
                    is_ok = False
            if is_ok and new_quests:
                response[idx] = res
                response[idx] += " в" if res == play else ""
                response[idx] += ' "' + new_quests[0].brief + '"'

    def __quest_append(
        self,
        npc: NPC,
        quest: Quest,
        data: Dict[str, Any],
        text: str,
        response: List[str],
    ) -> Tuple[str, List[str]]:
        """New quest appending to Protagonists questbook

        Parameters
        ----------
        npc : NPC
            The NPC that owns quest
        quest : Quest
            The receiving quest
        data : Dict[str, Any]
            Data loaded from db
        text : str
            The replica
        response : List[str]
            The list of responses to replica

        Returns
        -------
        Tuple[str, List[str]]
            Replica - responses pair
        """

        not_done_qids = [q.id for q in self.questbook if not q.is_done]
        if quest.id in not_done_qids:
            text = "Это задание уже у тебя есть"
            response = ["Аа, точно-точно"]
        else:
            my_quest = copy.deepcopy(quest)
            self.questbook.append(my_quest)
            if quest.kind == QuestKind.DELIVERY:
                items = [i for i in data["items"] if i.name == quest.item]
                if items:
                    quantity = quest.quantity if quest.quantity else 1
                    self.take(items[0], quantity)
            elif quest.kind in [QuestKind.UNION, QuestKind.UNION_AND_GRAB]:
                data["union"].append(npc)
        return text, response

    def quest_accept(self, quest: Quest, data: Dict[str, Any]) -> str:
        """Accepts a completed quest

        Parameters
        ----------
        quest : Quest
            Accepted quest
        data : Dict[str, Any]
            Data loaded from db

        Returns
        -------
        str
            Advancing experience and/or items message
        """

        text: str = self.advance_exp(quest.reward)
        text += f"\nКвест '{quest.brief}' завершён"
        if quest.kind in [QuestKind.DELIVERY, QuestKind.BATTLE_AND_DELIVERY]:
            items = [i for i in data["items"] if i.name == quest.item]
            if items:
                item = items[0]
                quantity = self.inventory[item]
                self.throw(item, quantity)

        if quest.reward_item and quest.reward_item_quantity:
            items = [
                i
                for i in data["items"] + data["weapons"]
                if i.name == quest.reward_item
            ]
            if items:
                item = items[0]
                qnt: int = quest.reward_item_quantity
                self.__item_transfer(data, item, qnt)
                text += f"\nВы получили {qnt} шт. {item.name}"
        quest.is_done = True
        self.__make_npc_quest_done(quest, data["npcs"])
        return text

    def __make_npc_quest_done(
        self, quest: Quest, characters: List[Union[NPC, Enemy]]
    ) -> None:
        """Records status - is done for a quest given by NPC

        Parameters
        ----------
        quest : Quest
            The completed quest
        characters : List[Union[NPC, Enemy]]
            The list of persons who could give the quest
        """

        npc_gives = [
            npc for npc in characters if npc.id == quest.giving_npc_id
        ]
        if npc_gives:
            for npc in npc_gives:
                for q in npc.questbook:
                    q.is_done = True if q.id == quest.id else q.is_done

    def check_quests(self, npc: NPC, data: Dict[str, Any]) -> str:
        """Сhecks whether the quest is finished or not

        Parameters
        ----------
        npc : NPC
            NPC to talk to
        data : Dict[str, Any]
            Data loaded from db
        """

        text: str = ""
        hero: Protagonist = self  # noqa: F841 necessary for eval
        checked_quests: List[Quest] = [
            q
            for q in self.questbook
            if not q.is_done and not q.kind == QuestKind.BATTLE
        ]
        for quest in checked_quests:
            if (
                quest.giving_npc_id
                and npc.id == quest.giving_npc_id
                or quest.receiving_npc_id
                and npc.id == quest.receiving_npc_id
            ):
                if eval(quest.condition):
                    text = self.quest_accept(quest, data)
        return text

    def __get_fresh_news(self, data: Dict[str, Any]) -> str:
        """Gets fresh news from database

        Parameters
        ----------
        data : Dict[str, Any]
            Data loaded from db

        Returns
        -------
        str
            The fresh news
        """

        news: Dict[str, str] = data["news"]
        max_range = len(news)
        text: str = r.choice(
            ["Рассказывали тут мне небылицу, слушай",
             "Проезжал тут иностранец, и вот что рассказал",
             "Услышал во сне голос, и вот что он мне сообщил",
             "Рассказали, сам не поверил",
             "Прочитал в старой книге"])
        text += ":\n\n"
        text += news[str(r.randint(1, max_range))]
        return text

    def attack(
        self,
        assaulted: Union[Protagonist, NPC, Enemy],
        data: Dict[str, Any],
        is_nested=False,
    ) -> str:
        """Calculating an attack on an assaulted

        Parameters
        ----------
        assaulted : Union[Protagonist, NPC, Enemy]
            The person being attacked
        data : Dict[str, Any]
            Data loaded from db
        is_nested : bool, optional
            Is this a nested function, by default False

        Returns
        -------
        str
            The result of attack
        """

        attacker: Union[Protagonist, NPC, Enemy] = self

        result = attacker.__attack_init_message(assaulted)
        result = "<u>" + result + "</u>" if not is_nested else result
        init_len: int = len(result)

        assaulted.pursuit_time = 5
        if assaulted not in data["pursuit"] and type(assaulted) is Enemy:
            data["pursuit"].append(assaulted)

        map_free = data["map_free"] + data["init"]["appearances"]
        attacker_damage: int = 0
        if attacker.is_in_range(assaulted, attacker.weapon.range):
            attacker_damage = attacker.__get_damage(assaulted)
        else:
            assaulted, message = attacker.__assaulted_not_in_range(
                assaulted, data, map_free
            )
            result = add_new_line(result, message)

        assaulted_damage: int = 0
        if assaulted.is_in_range(attacker, assaulted.weapon.range):
            assaulted_damage = assaulted.__get_damage(attacker)
        else:
            attacker, message = assaulted.__attacker_not_in_range(
                attacker, data, map_free
            )
            result = add_new_line(result, message)

        message = ""
        if attacker_damage or assaulted_damage:
            message = attacker.__hit_exchange(
                assaulted, attacker_damage, assaulted_damage, data
            )
        elif attacker_damage and attacker_damage == assaulted_damage:
            message = attacker.__damages_equal_message(assaulted)
        elif assaulted.hp <= 0:
            message = f"{assaulted.name} {Phrases.ENEMY_DEFEAT.value}"
        elif len(result) == init_len:
            message = "Вы" if type(attacker) is Protagonist else attacker.name
            message += " и "
            if type(assaulted) is Protagonist:
                message += "вы"
            else:
                message += assaulted.name
            message += " не нанесли друг другу урона"
        result = add_new_line(result, message)
        return result + "\n\n" if result[-2:] != "\n\n" else result

    def __attack_init_message(
        attacked: Union[Protagonist, NPC, Enemy],
        assaulted: Union[Protagonist, NPC, Enemy],
    ) -> str:
        """Initial attacking message

        Parameters
        ----------
        attacked : Union[Protagonist, NPC, Enemy]
            The attacker person
        assaulted : Protagonist, NPC, Enemy]
            The assaulted person

        Returns
        -------
        str
            Initial message
        """

        message: str = "Вы" if type(attacked) is Protagonist else attacked.name
        message += " атакует"
        message += "е " if type(attacked) is Protagonist else " "
        message += "Вас" if type(assaulted) is Protagonist else assaulted.name
        return message

    def __assaulted_not_in_range(
        attacker: Union[Protagonist, NPC, Enemy],
        assaulted: Union[Protagonist, NPC, Enemy],
        data: Dict[str, Any],
        map_free: List[str],
    ) -> Tuple[Union[Protagonist, NPC, Enemy], str]:
        """Handling situation when assaulted is outside attacker's range

        Parameters
        ----------
        attacker : Union[Protagonist, NPC, Enemy]
            The attacker person
        assaulted : Union[Protagonist, NPC, Enemy]
            The assaulted person
        data : Dict[str, Any]
            Data loaded from db
        map_free : List[str]
            List of symbols that an attacker can stand on

        Returns
        -------
        Tuple[Union[Protagonist, NPC, Enemy], str]
            The assaulted person and info message pair
        """

        field: List[List[str]] = data["fields"][attacker.location_id - 1]
        is_moved: bool = False
        is_change_assaulted: bool = False
        weakest: Optional[Union[Protagonist, NPC, Enemy]] = None
        if type(attacker) is Enemy:
            weakest = attacker.choose_weakest(data, assaulted)
            range_to_assaulted = attacker.__calc_range(assaulted)
            range_to_weakest = attacker.__calc_range(weakest)
            if range_to_assaulted > range_to_weakest:
                assaulted = weakest
                if attacker.rapprochement(weakest, field, map_free):
                    is_change_assaulted = True
                    is_moved = True
            elif attacker.rapprochement(assaulted, field, map_free):
                is_moved = True
        elif type(attacker) is NPC:
            if attacker.rapprochement(assaulted, field, map_free):
                is_moved = True
        info: str = attacker.not_in_range_message(
            assaulted, is_moved, is_change_assaulted, data
        )
        return assaulted, info

    def __attacker_not_in_range(
        assaulted: Union[Protagonist, NPC, Enemy],
        attacker: Union[Protagonist, NPC, Enemy],
        data: Dict[str, Any],
        map_free: List[str],
    ) -> Tuple[Union[Protagonist, NPC, Enemy], str]:
        """Handling situation when attacker is outside assaulted's range

        Parameters
        ----------
        assaulted : Union[Protagonist, NPC, Enemy]
            The assaulted person
        attacker : Union[Protagonist, NPC, Enemy]
            The attacker person
        data : Dict[str, Any]
            Data loaded from db
        map_free : List[str]
            List of symbols that an assaulted can stand on

        Returns
        -------
        Tuple[Union[Protagonist, NPC, Enemy], str]
            The attacker person and info message pair
        """

        field: List[List[str]] = data["fields"][assaulted.location_id - 1]
        is_moved: bool = False
        is_change_assaulted: bool = False
        if type(assaulted) is not Protagonist:
            weakest = assaulted.choose_weakest(data, attacker)
            range_to_attacked = assaulted.__calc_range(attacker)
            range_to_weakest = assaulted.__calc_range(weakest)
            if range_to_attacked > range_to_weakest:
                attacker = weakest
                if assaulted.rapprochement(weakest, field, map_free):
                    is_change_assaulted = True
                    is_moved = True
            elif assaulted.rapprochement(attacker, field, map_free):
                is_moved = True

        info: str = assaulted.not_in_range_message(
            attacker, is_moved, is_change_assaulted, data
        )
        return attacker, info

    def not_in_range_message(
        attacker: Union[Protagonist, NPC, Enemy],
        assaulted: Union[Protagonist, NPC, Enemy],
        is_moved: bool,
        is_change_assaulted: bool,
        data: Dict[str, Any],
    ) -> str:
        """Creates message if attackers and assaulted not in range

        Attacker attacks new assaulted if new assaulted in range

        Parameters
        ----------
        attacker : Union[Protagonist, NPC, Enemy]
            The attacker person
        assaulted : Union[Protagonist, NPC, Enemy]
            The assaulted person
        is_moved : bool
            True if attacker moved
        is_change_assaulted : bool
            True if assaulted person changed
        data : Dict[str, Any]
            Data loaded from db

        Returns
        -------
        str
            Information message about attacker moved and/or changed assaulted
        """

        info: str = ""
        if is_moved:
            info = f"{attacker.name} идёт к "
            info += "Вам" if type(assaulted) is Protagonist else assaulted.name
        if is_change_assaulted:
            info += ", потому что "
            info += "вы" if type(assaulted) is Protagonist else ""
            info += " ближе"
            if attacker.is_in_range(assaulted, assaulted.weapon.range):
                info += "\n"
                is_nested = True
                info += attacker.attack(assaulted, data, is_nested)
        return info

    def is_in_range(
        self, person: Union[Protagonist, NPC, Enemy], cmpr: int
    ) -> bool:
        """Returns whether person is within the range of comparator

        Parameters
        ----------
        person : Union[Protagonist, NPC, Enemy]
            The given NPC

        cmpr : int
            The comparison range

        Returns
        -------
        bool
            True if NPC in range
        """

        res: bool = False
        if self.location_id == person.location_id and self.hp > 0:
            pos: Direction = self.whereami()
            pos_p: Direction = person.whereami()
            if (pos.x - pos_p.x) ** 2 + (pos.y - pos_p.y) ** 2 <= cmpr**2:
                res = True

        return res

    def __calc_range(self, person: Union[Protagonist, NPC, Enemy]) -> float:
        """Calculates the range value between persons

        Parameters
        ----------
        person : Union[Protagonist, NPC, Enemy]
            The person with whom the distance is calculated

        Returns
        -------
        float
            The distance between persons
        """

        pos: Direction = self.whereami()
        pos_p: Direction = person.whereami()
        return ((pos.x - pos_p.x) ** 2 + (pos.y - pos_p.y) ** 2) ** 0.5

    def __get_damage(self, enemy: Union[Protagonist, NPC, Enemy]) -> int:
        """Calculates the damage value

        Parameters
        ----------
        enemy : Union[Protagonist, NPC, Enemy]
            The person being attacked

        Returns
        -------
        int
            The damage value
        """

        level_part: int = math.ceil(self.level / 6 * r.randint(1, 6))
        weapon_part: int = r.randint(self.weapon.dmg_min, self.weapon.dmg_max)
        armor_part: int = math.floor(enemy.armor.buff / 3 * r.randint(0, 3))
        total: int = level_part + 2 * weapon_part - armor_part
        return total if total > 0 else 0

    def choose_weakest(
        self,
        data: Dict[str, Any],
        cur_person: Union[Protagonist, NPC, Enemy],
        attack_range=5,
    ) -> Union[Protagonist, NPC, Enemy]:
        """Chooses the weakest person to attack

        Parameters
        ----------
        data : Dict[str, Any]
            Data loaded from db
        cur_person: Union[Protagonist, NPC, Enemy]
            The current attacker or assaulted person
        attack_range : int, optional
            The range of choice the weakest person

        Returns
        -------
        Union[Protagonist, NPC, Enemy]
            The weakest person in range
        """

        npc: Union[Protagonist, NPC, Enemy] = cur_person
        npcs: List[Union[Protagonist, NPC, Enemy]] = []
        if self.weapon.range > attack_range:
            attack_range = self.weapon.range
        if type(self) is Enemy:
            unions = data.get("unions", [])
            npcs = [
                n
                for n in unions
                if n.hp > 0 and self.is_in_range(n, attack_range)
            ] + [data["hero"]]
        else:
            npcs = [
                e
                for e in data["enemies"]
                if e.hp > 0 and self.is_in_range(e, attack_range)
            ]
        if npcs:
            min_hp = min([n.hp for n in npcs])
            npcs = [n for n in npcs if n.hp == min_hp]
            if npcs:
                npc = npcs[0]
        if npc is None:
            logging.info("Weakest person did not found")
        return npc

    def rapprochement(
        self,
        person: Union[Protagonist, NPC, Enemy],
        field: List[List[str]],
        map_free: List[str],
    ) -> bool:
        """Rapprochement self closer to a person by 1 cell

        Parameters
        ----------
        person: Union[Protagonist, NPC, Enemy]
            The person with whom the rapprochement occurs
        field: List[List[str]]
            The current location where the events take place
        map_free: List[str]
            List of symbols that an person can stand on

        Returns
        -------
        bool
            Did the rapprochement really happen
        """

        is_new_pos: bool = False
        pos: Direction = self.whereami()
        pos_p: Direction = person.whereami()
        new_pos: Optional[Direction] = None
        calc_field = self.calc_paths(field, pos, map_free, pos_p)
        new_pos = self.get_next_position(
            calc_field, field, map_free, pos, pos_p
        )
        if new_pos:
            check: Position = self.is_correct_pos(field, map_free, new_pos)
            if check == Position.CORRECT:
                self.go(new_pos)
                is_new_pos = True
            else:
                logging.info(f"{self.name} try to go out field")
        return is_new_pos

    def is_correct_pos(
        self, field: List[List[str]], map_free, new_pos: Direction
    ) -> Position:
        """Checks the correctness of the given position

        Parameters
        ----------
        field : List[List[str]]
            The current location where the position checks
        map_free : _type_
            List of characters in which the position is correct
        new_pos : Direction
            The checked position

        Returns
        -------
        Position
            The checked status
        """

        check: Position = Position.CORRECT
        y_max: int = len(field) - 1
        correct_y_borders: bool = new_pos.y <= y_max and new_pos.y >= 0
        correct_x_borders: bool = False
        if correct_y_borders:
            x_max: int = len(field[y_max - new_pos.y]) - 1
            correct_x_borders = new_pos.x >= 0 and new_pos.x <= x_max
        if correct_x_borders and correct_y_borders:
            if field[y_max - new_pos.y][new_pos.x] not in map_free:
                check = Position.OBSTACLE
        else:
            check = Position.OUT_FIELD
        return check

    def calc_paths(
        self,
        field: List[List[str]],
        pos: Direction,
        map_free: List[str],
        end=None,
    ) -> List[List[int]]:
        """Calculates the distances from start position

        If the end position is specified - the calculation is only from
        start to end position

        Parameters
        ----------
        field : List[List[str]]
            The current location where the calculations take place
        pos : Direction
            The start position
        map_free : List[str]
            List of characters that can be used to build a path
        end : Direction, optional
            The end position

        Returns
        -------
        List[List[int]]
            The matrix with calculated distances
        """

        y: int = len(field)
        x: int = len(field[0]) if field else 0
        inf: int = x * y + 1
        obstacle: int = -1
        calc_field: List[List[int]] = [
            [inf for _ in range(x)] for _ in range(y)
        ]
        calc_field[pos.y][pos.x] = 0
        directions = [
            Direction(-1, 0),
            Direction(0, 1),
            Direction(1, 0),
            Direction(0, -1),
        ]

        def cell_handle(cell: Direction, value: int) -> None:
            """Writes to cell actual distance

            Parameters
            ----------
            cell : Direction
                The current cell
            value: int
                The previous cells distance
            """

            check = self.is_correct_pos(field, map_free, cell)
            if (
                check != Position.OUT_FIELD
                and calc_field[new_pos.y][new_pos.x] == inf
            ):
                res: int = inf - 1
                if check == Position.CORRECT:
                    res = value + 1
                    deq.append(new_pos)
                elif check == Position.OBSTACLE:
                    res = obstacle
                calc_field[new_pos.y][new_pos.x] = res

        deq = deque([pos])
        is_find: bool = False  # if end is normal position
        while deq and not is_find:
            cell = deq.popleft()
            if self.is_correct_pos(field, map_free, cell) == Position.CORRECT:
                value = calc_field[cell.y][cell.x]
                for dir in directions:
                    new_pos: Direction = Direction(
                        cell.x + dir.x, cell.y + dir.y
                    )
                    cell_handle(new_pos, value)
                    if end and new_pos == end:
                        is_find = True
                        break
        return calc_field

    def get_next_position(
        self,
        calc_field: List[List[int]],
        field: List[List[str]],
        map_free: List[str],
        pos: Direction,
        pos_p: Direction,
    ) -> Direction:
        """Gets the smallest distance cell from start to end position

        Parameters
        ----------
        calc_field : List[List[int]]
            The matrix with calculated distances
        field : List[List[str]]
            The current location where the calculations take place
        map_free : List[str]
            List of characters that can be used to build a path
        pos : Direction
            The start position
        pos_p : Direction
            The end position

        Returns
        -------
        Direction
            Next position for the fastest rapprochement
        """

        def make_path() -> List[Direction]:
            """Chooses the fastest path from start to end

            Returns
            -------
            List[Direction]
                The fastest path
            """

            path: List[Direction] = [pos_p]
            value = calc_field[pos_p.y][pos_p.x]
            cell: Direction = pos_p
            while value != 0:
                value, new_cell = get_min_value(cell)
                path.append(new_cell) if value else None
                cell = new_cell
            return path

        def get_min_value(cell: Direction) -> Tuple[int, Direction]:
            """Selects the cell with smallest value in adjacent cells

            Parameters
            ----------
            cell : Direction
                The cell to inspection

            Returns
            -------
            Tuple[int, Direction]
                The minimal value and its cell
            """

            min_val: int = calc_field[cell.y][cell.x]
            min_pos: Direction = cell
            for p in self.pass_adjacent_сells(cell, ignore_diagonals=True):
                if self.is_correct_pos(field, map_free, p) == Position.CORRECT:
                    cur_value = calc_field[p.y][p.x]
                    if cur_value < min_val and cur_value >= 0:
                        min_val = cur_value
                        min_pos = p
            return min_val, min_pos

        path = make_path()
        return path[-1] if path else pos

    def pass_adjacent_сells(
        self, pos: Direction, side=3, ignore_diagonals=False
    ) -> Iterator[Direction]:
        """Passing through adjacent cells of a given cell

        Parameters
        ----------
        pos : Direction
            The given cell
        side : int, optional
            The side of the square along which passing, by default 3
        ignore_diagonals : bool
            If it is forbidden to walk diagonally, by default False

            4   5   6   7   8
            3   2   3   4   9
            2   1  pos  5  10
            1   0   7   6  11
            0  15  14  13  12


        Yields
        ------
        Iterator[Direction]
            The next cell clockwise
        """

        left_vertical: int = side - 1
        up_gorizontal: int = 2 * (side - 1)
        right_vertical: int = 3 * (side - 1)
        down_gorizontal: int = 4 * (side - 1) - 1
        for i in range(4 * side - 4):
            shift: int = side // 2
            if i <= left_vertical:
                new_pos = Direction(pos.x - shift, pos.y + i - shift)
            elif i <= up_gorizontal:
                i -= left_vertical
                new_pos = Direction(pos.x + i - shift, pos.y + shift)
            elif i <= right_vertical:
                i -= up_gorizontal
                new_pos = Direction(pos.x + shift, pos.y + shift - i)
            elif i <= down_gorizontal:
                i -= right_vertical
                new_pos = Direction(pos.x + shift - i, pos.y - shift)

            if ignore_diagonals and i in [
                0,
                left_vertical,
                up_gorizontal,
                right_vertical,
            ]:
                new_pos = Direction(-1, -1)
            yield new_pos

    def __damages_equal_message(
        attacker: Union[Protagonist, NPC, Enemy],
        assaulted: Union[Protagonist, NPC, Enemy],
    ) -> str:
        """Returns information message damages are equal

        Parameters
        ----------
        attacker : Union[Protagonist, NPC, Enemy]
            The attacker person
        assaulted : Union[Protagonist, NPC, Enemy]
            The assaulted person

        Returns
        -------
        str
            The message
        """

        messages: List[str] = []
        message = "Вы" if type(attacker) is Protagonist else attacker.name
        message += f" и {assaulted.name}"
        messages.append(f"{message} оба промахнулись!")
        messages.append(f"{message} оба увернулись")
        return r.choice(messages)

    def __hit_exchange(
        attacker: Union[Protagonist, NPC, Enemy],
        assaulted: Union[Protagonist, NPC, Enemy],
        attacker_dmg: int,
        assaulted_dmg: int,
        data: Dict[str, Any],
    ) -> str:
        """If attacker or assaulted has non-zero damage

        Parameters
        ----------
        attacker : Union[Protagonist, NPC, Enemy]
            The attacker person
        assaulted : Union[Protagonist, NPC, Enemy]
            The assaulted person
        attacker_dmg : int
            The attackers damage
        assaulted_dmg : int
            The assaulted damage
        data : Dict[str, Any]
            Data loaded from db

        Returns
        -------
        str
            Message about how the exchange of hits was carried out
        """

        message: str = ""
        try:
            assaulted.take_hit(attacker_dmg)
            attacker.take_hit(assaulted_dmg)
            message = attacker.__hit_exchange_message(
                assaulted, attacker_dmg, assaulted_dmg
            )
        except Exception as e:
            if attacker.__is_person_died(assaulted, Enemy):
                if type(assaulted) is Enemy:
                    message = attacker.__enemy_defeat(assaulted, data)
                elif type(attacker) is Enemy:
                    message = assaulted.__enemy_defeat(attacker, data)
            elif attacker.__is_person_died(assaulted, Protagonist):
                message = str(e)
            elif attacker.__is_person_died(assaulted, NPC):
                message = f"{attacker.name} повержен"
                if attacker in data["union"]:
                    data["union"].remove(attacker)
                elif assaulted in data["union"]:
                    data["union"].remove(attacker)
        return message

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
            raise Exception(Phrases.DEFEAT.value)

    def __hit_exchange_message(
        attacker: Union[Protagonist, NPC, Enemy],
        assaulted: Union[Protagonist, NPC, Enemy],
        attacker_dmg: int,
        assaulted_dmg: int,
    ) -> str:
        """Information about how the exchange of hits was carried out

        Parameters
        ----------
        attacker : Union[Protagonist, NPC, Enemy]
            The attacker person
        assaulted : Union[Protagonist, NPC, Enemy]
            The assaulted person
        attacker_dmg : int
            The attackers damage
        assaulted_dmg : int
            The assaulted damage

        Returns
        -------
        str
            Message about how the exchange of hits was carried out
        """

        is_hero: bool = True if type(assaulted) is Protagonist else False
        message = "Вы" if type(assaulted) is Protagonist else assaulted.name
        if attacker_dmg:
            message += " теряет"
            message += "е" if is_hero else ""
            message += f" {attacker_dmg} hp"
        else:
            message += " не получает"
            message += "е" if is_hero else ""
            message += " урона"

        message += "\n"
        if is_hero:
            message += f"У вас {assaulted.hp} здоровья"
        else:
            message += assaulted.__enemy_secret_hp()
        message += "\n"

        is_hero = True if type(attacker) is Protagonist else False
        message += "Вы" if is_hero else attacker.name
        if assaulted_dmg:
            message += " теряет"
            message += "е" if is_hero else ""
            message += f" {assaulted_dmg} hp"
        else:
            message += " не получает"
            message += "е" if is_hero else ""
            message += " урона"

        message += "\n"
        if is_hero:
            message += "Ваше здоровье"
            message += f" {attacker.hp} hp"
        else:
            message += attacker.__enemy_secret_hp()
        return message

    def __enemy_secret_hp(self) -> str:
        """Hides enemy's actual hit points

        Returns
        -------
        str
            The informational message about enemies hit points
        """

        status: str = "\n"
        if self.hp > INIT_HP * (1 + self.level / 2) * 0.75:
            status = "полно"
        elif self.hp > INIT_HP * (1 + self.level / 2) * 0.4:
            status = "хватает"
        else:
            status = "мало"
        return f"У него {status} здоровья"

    def __enemy_defeat(self, enemy: Enemy, data: Dict[str, Any]) -> str:
        """Handles the case of an enemy's death in battle.

        Parameters
        ----------
        enemy : Enemy
            The defeated enemy
        data : Dict[str, Any]
            Data loaded from db

        Returns
        -------
        str
            The informational message about experience, quest status
            and received items
        """

        exp: int = int(LEVEL_EXP / 3 * enemy.level)
        result = f"{enemy.name} {Phrases.ENEMY_DEFEAT.value}\n"
        take_exp_range: int = 5
        for npc in data["union"]:
            if npc.hp > 0 and npc.is_in_range(enemy, take_exp_range):
                result += npc.advance_exp(exp) + "\n"
        if data["hero"].is_in_range(enemy, take_exp_range):
            result += data["hero"].advance_exp(exp)
            result += " за победу над врагом"

        for quest in [q for q in self.questbook if not q.is_done]:
            if quest.kind == QuestKind.BATTLE and quest.condition is not None:
                eval_condition: bool = eval(quest.condition)
                if eval_condition:
                    text: str = f"Квест {quest.brief} завершён\n"
                    result = add_new_line(result, text)
                    result += self.advance_exp(quest.reward)
                    quest.is_done = True
                    self.__make_npc_quest_done(quest, data["npcs"])

        enemy.pursuit_time = 0
        if enemy in data["pursuit"]:
            data["pursuit"].remove(enemy)
        return result

    def __is_person_died(
        attacker: Union[Protagonist, NPC, Enemy],
        assaulted: Union[Protagonist, NPC, Enemy],
        person_type: Union[Type[Protagonist], Type[NPC], Type[Enemy]],
    ) -> bool:
        """Checks if a person dead in battle

        Parameters
        ----------
        attacker : Union[Protagonist, NPC, Enemy]
            The attacker person
        assaulted : Union[Protagonist, NPC, Enemy]
            The assaulted person
        person_type : Union[Protagonist, NPC, Enemy]
            Type of person to compare

        Returns
        -------
        bool
            True if died
        """

        return (attacker.hp <= 0 and type(attacker) is person_type) or (
            assaulted.hp <= 0 and type(assaulted) is person_type
        )

    def heal(self, value=1) -> str:
        """Increase health points

        Parameters
        ----------
        value : int, optional
            The strength of heal, by default 1

        Returns
        -------
        str
            The infomational message about healed hit points
        """

        self.hp += value
        return f"Прибавлено {value} hp"

    def advance_exp(self, value: int) -> str:
        """Increase experience level and check level up

        Parameters
        ----------
        value : int
            The experience value

        Returns
        -------
        str
            The infomational message about advanced experience
        """

        result: str = ""
        if type(self) is Protagonist:
            result += "Вы получили"
        else:
            result += f"{self.name} получил"
        result += f" {value} опыта"
        self.exp += value
        threshold: int = self.level * 1000
        while self.exp >= threshold:
            result += "\n" + self.advance_level()
            self.exp -= threshold
            self.exp = 0 if self.exp < 0 else self.exp
            threshold = self.level * 1000
        return result

    def advance_level(self, value=1) -> str:
        """Increase level

        Parameters
        ----------
        value : int, optional
            The increase level, by default 1

        Returns
        -------
        str
            The infomational message about advanced level
        """

        self.level += value
        result: str = f"Теперь у Вас {self.level} уровень"
        self.hp = int(INIT_HP * (1 + self.level / 2))
        return result

    def go(self, direction: Direction) -> None:
        """Changes the position of character

        Parameters
        ----------
        direction : Direction
            New current position
        """

        self.__pos = direction

    def union_handle(
        self, field: List[List[str]], map_free: List[str], npc: NPC
    ) -> None:
        """Processing the movement of NPCs who are in an alliance

        NPC is located on the first free cell clockwise

        Parameters
        ----------
        field : List[List[str]]
            The current location where the protagonist in
        map_free : List[str]
            List of characters that NPC can stand on
        npc : NPC
            The NPC in union

        2  3  4
        1 pos 5
        0  7  6
        """

        pos: Direction = self.whereami()
        if npc.is_in_range(self, 2):
            generator = self.pass_adjacent_сells(pos)
            for possible_pos in generator:
                check = self.is_correct_pos(field, map_free, possible_pos)
                if check == Position.CORRECT:
                    new_pos = possible_pos
                    npc.go(new_pos)
                    break
        else:
            npc.rapprochement(self, field, map_free)

    def pursuit_handle(
        self,
        enemy: Enemy,
        field: List[List[str]],
        map_free: List[str],
        persecuted: List[Enemy],
    ) -> str:
        """Processing the movement of NPCs that are being pursued

        Parameters
        ----------
        enemy : Enemy
            The enemy in pursuit
        field : List[List[str]]
            The current location where the protagonist in
        map_free : List[str]
            List of characters that enemy can stand on
        persecuted: List[Enemy]:
            List of enemies that haunt the protagonist

        Returns
        -------
        str
            If the enemy is within the protagonists attack range
        """

        text: str = ""
        if enemy.pursuit_time > 0:
            chance: int = r.randint(0, 1)
            if not enemy.is_in_range(self, enemy.weapon.range) and chance:
                enemy.rapprochement(self, field, map_free)
            if enemy.is_in_range(self, enemy.weapon.range):
                text = f"Вас преследует {enemy.name}\n"
        enemy.pursuit_time -= 1
        if enemy.pursuit_time <= 0:
            persecuted.remove(enemy) if enemy in persecuted else None
        return text

    def whereami(self) -> Direction:
        """Returns current position

        Returns
        -------
        Direction
            The current position
        """

        return self.__pos

    def set_pos(self, x: int, y: int) -> None:
        """Sets itself a new position

        Parameters
        ----------
        x : int
            The x coordinate of the position
        y : int
            The y coordinate of the position
        """

        self.__pos = Direction(x, y)

    def take(self, item: Union[Item, Weapon], quantity=1) -> None:
        """Takes the item

        Parameters
        ----------
        item : Union[Item, Weapon]
           Taken item
        """

        self.inventory[item] += quantity

    def throw(self, item: Union[Item, Weapon], quantity=1) -> None:
        """Dropping an item and losing it

        Parameters
        ----------
        item : Union[Item, Weapon]
            The throwing item
        quantity : int, optional
            The quatity to throw, by default 1
        """

        inv = self.inventory
        check_item = inv.get(item, None)
        if check_item and quantity > 0:
            inv[item] -= quantity
            if inv[item] <= 0:
                del inv[item]
                self.wear_best_equip(item)

    def wear_best_equip(self, item: Union[Item, Weapon]) -> None:
        """Wears another armor or choose another weapon

        If the current armor or weapon is discarded, its best analogue
        is selected

        Parameters
        ----------
        item : Union[Item, Weapon]
            The discarded item
        """

        if self.weapon == item:
            weapons = [w for w in self.inventory if type(w) is Weapon]
            if weapons:
                weapons.sort(key=lambda w: w.dmg_max)
                self.weapon = weapons[-1]
            else:
                text: str = f"{self.name} standart weapon did not found"
                logging.error(text)
        elif self.armor == item:
            armors = [
                a
                for a in self.inventory
                if type(a) is Item and a.buff_parameter == ItemBuff.DEFENSE
            ]
            if armors:
                armors.sort(key=lambda a: a.buff)
                self.armor = armors[-1]
            else:
                text = f"{self.name} standart armor did not found"
                logging.error(text)

    def give(self, npc: NPC, item: Union[Item, Weapon], quantity=1) -> None:
        """Give the item

        Parameters
        ----------
        npc : NPC
            The receiving NPC
        item : Union[Item, Weapon]
            Given item
        quantity : int, optional
            The giving quantity, by default 1
        """

        self.throw(item, quantity)
        npc.receive(item, quantity)

    def loot(self, name: str, data: Dict[str, Any], npcs: List[NPC]) -> str:
        """Takes item from person and deletes person from list

        Parameters
        ----------
        name : str
            The name of looted person
        data : Dict[str, Any]
            Data loaded from db
        npcs : List[NPC]
            List of NPCs the person is in

        Returns
        -------
        str
            The informational message about looted status
        """

        text: str = ""
        persons = [p for p in npcs if p.name == name]
        if persons:
            text = f"Вы забрали снаряжение у {name}"
            person = persons[0]
            quests = [
                q
                for q in self.questbook
                if not q.is_done
                and q.kind
                in [QuestKind.UNION_AND_GRAB, QuestKind.FIND_AND_GRAB]
            ]
            inventory = copy.deepcopy(person.inventory)
            for i, q in inventory.items():
                if i not in [data["std_weapon"], data["std_armor"]]:
                    self.__item_transfer(data, i, q)
                    for qst in quests:
                        text += self.__loot_quest_handle(data, person, qst, i)

            for quest in [
                q
                for q in person.questbook
                if not q.is_done and q.kind == QuestKind.BATTLE_AND_DELIVERY
            ]:
                my_quest = copy.deepcopy(quest)
                self.questbook.append(my_quest)
                quest.is_done = True
                text += f"\nВы получили квест '{quest.brief}'"

            person.inventory = {}
            npcs.remove(person)
        else:
            text = "Вы слишком далеко"
            logging.info("Lootable person did not found")
        return text

    def __item_transfer(
        self,
        data: Dict[str, Any],
        item: Union[Item, Weapon],
        quantity: int,
    ) -> str:
        """Adds item to self inventory if looted person has item

        Parameters
        ----------
        data : Dict[str, Any]
            Data loaded from db
        item : Union[Item, Weapon]
            The adding item
        quantity : int
            The quantity of item
        """

        is_new: bool = True
        for i in self.inventory:  # because different objects with same name
            if i.name == item.name:
                self.inventory[i] += quantity
                is_new = False
                break
        if is_new:
            if not item.is_tradable:
                item = self.__try_get_tradable_item(item, data["items"])
            self.inventory[item] = quantity

    def __loot_quest_handle(
        self,
        data: Dict[str,
                   Any],
        person: Union[NPC,
                      Enemy],
        quest: Quest,
        item: Union[Item, Weapon]
    ) -> str:
        """Checks quest accepting when looting the person

        Parameters
        ----------
        data : Dict[str, Any]
            Data loaded from db
        person : Union[NPC, Enemy]
            The lootable person
        quest : Quest
            The quest to inspection
        item : Union[Item, Weapon]
            The item to inspection

        Returns
        -------
        str
            The informational message about quest accepting
        """

        text: str = ""
        hero: Protagonist = self  # noqa: F841 necessary for eval
        if quest.item and quest.item == item.name:
            if quest.receiving_npc_id and quest.receiving_npc_id == person.id:
                if quest.condition and eval(quest.condition):
                    text += "\n" + self.quest_accept(quest, data)
        return text

    def __try_get_tradable_item(
        self, item: Union[Item, Weapon], items: List[Item]
    ) -> Union[Item, Weapon]:
        """Try find tradable item analogue

        Parameters
        ----------
        item : Union[Item, Weapon]
            Incoming item
        items : List[Item]
            The list of all items

        Returns
        -------
        Union[Item, Weapon]
            The outcoming item
        """

        result: Union[Item, Weapon] = item
        for i in items:
            if i.name == item.name and i.is_tradable:
                result = i
        return result

    def get_person_info(self) -> str:
        """Gets person's class, level, name, appearance and hp info

        Returns
        -------
        str
            Informational message
        """

        cls_name: str = "".join(
            [name for name, v in PLAYABLE_CLS.items() if v == self.class_id]
        )
        text: str = (
            f"{cls_name} {self.level} lvl {self.name} {self.appearance} "
            f"[{self.hp} ❤️]"
        )
        return text


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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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
        quantity : int, optional
            The receiving quantity, by default 1
        """

        self.take(item, quantity)

    def give(
        self, hero: Protagonist, item: Union[Item, Weapon], quantity=1
    ) -> None:
        """Give the item to hero

        Parameters
        ----------
        hero : Protagonist
            The game protagonist
        item : Union[Item, Weapon]
            Given item
        quantity : int, optional
            The giving quantity, by default 1
        """

        init_quantity: int = quantity
        if item is not None:
            self.inventory[item] -= quantity
            if self.inventory[item] <= 0:
                quantity = self.inventory[item]
                del self.inventory[item]
            hero.take(item, init_quantity)


class Enemy(NPC):
    """The enemy NPC class"""

    pass


def add_new_line(result: str, new_part: str) -> str:
    """Adds line before new part if old part does not end with new line

    Parameters
    ----------
    result : str
        The old part
    new_part : str
        The new part of result

    Returns
    -------
    str
        Concatenated result
    """

    if new_part:
        if result[-1] != "\n":
            result += "\n"
        result += new_part
    return result
