def add_ingot(purse):
    new_purse = dict(purse)
    if "gold_ingots" not in purse:
        new_purse["gold_ingots"] = 1
    else:
        new_purse["gold_ingots"] += 1
    return new_purse


def get_ingot(purse):
    new_purse = dict(purse)
    if "gold_ingots" in purse and purse["gold_ingots"] > 0:
        new_purse["gold_ingots"] -= 1
    return new_purse


def empty(purse):
    return {}
