def check(lst):
    return [i for i in lst if isinstance(i, str)]


def fix_wiring(cables, sockets, plugs):
    return [
        (
            f"plug {check(cables)[i]} into {check(sockets)[i]} using {check(plugs)[i]}"
            if len(check(plugs)) > i
            else f"weld {cables[i]} to {sockets[i]} without plug"
        )
        for i in range(len(check(cables)))
    ]


def main(cables, sockets, plugs):
    for c in fix_wiring(cables, sockets, plugs):
        print(c)


if __name__ == "__main__":
    plugs = ["plug1", "plug2", "plug3"]
    sockets = ["socket1", "socket2", "socket3", "socket4"]
    cables = ["cable1", "cable2", "cable3", "cable4"]

    plugs2 = ["plugZ", None, "plugY", "plugX"]
    sockets2 = [1, "socket1", "socket2", "socket3", "socket4"]
    cables2 = ["cable2", "cable1", False]

    print("---------------------------------------------")
    main(cables, sockets, plugs)
    print("---------------------------------------------")
    main(cables2, sockets2, plugs2)
