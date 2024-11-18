"""The module loads all the data needed for the game

The script requires load_data to load game characters and everything
that belongs to them, load_map - for loading game locations
"""

from load_data import loader
from load_map import load_fields
from character_classes import Protagonist, NPC, QuestKind
from typing import Dict, List, Any


def load_all(
    data: Dict[str, Any], save_id=1, args=None, is_init_load=False
) -> Dict[str, Any]:
    """Interface for loader from PostgreSQL and loads another game data

    Parameters
    ----------
    data: Dict[str, Any]
        Dictionary with init information
    save_id : int, optional
        Load with modified parameters from saves or not, by default 1
    args : Namespace, optional
        Need or not drop database, change or append values,
        by default None
    is_init_load : bool, optional
        Is starts game from load, by default False

    Returns
    -------
    Dict[str, Any]
        The dictionary with all game needed data
    """

    all_data = loader(data, save_id, args, is_init_load)
    all_data["fields"] = load_fields()
    all_data["union"] = get_npcs_in_union(all_data["hero"], all_data["npcs"])
    all_data["pursuit"] = [n for n in data["enemies"] if n.pursuit_time]
    return all_data


def get_npcs_in_union(hero: Protagonist, npcs: List[NPC]) -> List[NPC]:
    """Loads NPCs that in alliance

    Parameters
    ----------
    hero : c.Protagonist
        The playable character
    npcs : List[NPC]
        The dictionary with enemies and NPCs lists

    Returns
    -------
    List[c.NPC]
        List of NPCs that are allied with protagonist
    """

    return [
        n
        for q in hero.questbook
        if not q.is_done
        and q.kind in [QuestKind.UNION, QuestKind.UNION_AND_GRAB]
        for n in npcs
        if n.id == q.giving_npc_id
    ]
