import sqlite3
import logging
from collections import defaultdict


class Direction:
    """
    Directional movement to
    """

    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class SubLocation:
    """
    Sub-location in game world
    """

    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description

    def get_description(self):
        return self.description


class Location:
    """
    Location in game world
    """

    def __init__(self, id: str, description: str):
        """
        This attribute is a dictionary that will store the relationships between the current location and other locations.
        The dictionary keys will be directions (e.g. “north”) and the values will be objects of other locations that can be contacted.
        """
        self.id = id
        self.description = description
        self.connections = {}
        self.sub_locations = {}

    def connect(self, direction: str, location: "Location"):
        """
        This method allows you to establish a link between the current location and another location in a given direction.
        """
        self.connections[direction] = location

    def add_sub_location(self, sub_location: SubLocation):
        self.sub_locations[sub_location.id] = sub_location

    def get_description(self):
        """
        This method returns a description of the current location.
        """
        return self.description

    def get_sub_location(self):
        return self.sub_locations


class MatrixSub(SubLocation):
    def __init__(self, id: str, description: str):
        super().__init__(id, description)
        self.grid_size = 20
        self.position = (0, 0)
        self.characters = []

    def move(self, direction: str):
        x, y = self.position
        if direction == Direction.WEST and y > 0:
            self.position = (x, y - 1)
        elif direction == Direction.EAST and y < self.grid_size - 1:
            self.position = (x, y + 1)
        elif direction == Direction.SOUTH and x < self.grid_size - 1:
            self.position = (x + 1, y)
        elif direction == Direction.NORTH and x > 0:
            self.position = (x - 1, y)
        else:
            print("Вы не можете двигаться в этом направлении.")
        print(f"Вы находитесь в позиции {self.position}")

    def get_position(self):
        return self.position

    def get_matrix_representation(self):
        matrix = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        x, y = self.position
        matrix[x][y] = "*"

        for character in self.characters:
            char_x, char_y = character.pos
            if 0 <= char_x < self.grid_size and 0 <= char_y < self.grid_size:
                matrix[char_x][char_y] = "P"
        return "\n".join(" ".join(row) for row in matrix)


class Protagonist:
    def __init__(self, name: str, id: str, start_location: Location):
        self.id = id
        self.name = name
        self.hp = 10
        self.strength = 1
        self.craft = 1
        self.inventory = defaultdict(int)
        self.inventory["pocket dust"] += 1
        self.current_location = start_location  # Начальная локация

    def go(self, direction: str):
        if direction in self.current_location.connections:
            self.current_location = self.current_location.connections[direction]
            self.position = (0, 0)
            print(self.whereami())
            self.show_sub_location()
        else:
            print("Вы не можете пойти в этом направлении.")

    def whereami(self):
        return self.current_location.get_description()

    def display_current_location(self):
        print(f"\nВы находитесь в: {self.current_location.get_description()}")
        print("Куда вы можете пойти:")
        for direction in self.current_location.connections.keys():
            print(f"- {direction}")

        self.show_sub_location()

    def show_sub_location(self):
        sub_location = self.current_location.get_sub_location()
        if sub_location:
            print("Подлокации:")
            for sub_loc in sub_location.values():
                print(sub_loc.get_description())
                if isinstance(sub_loc, MatrixSub):
                    print(
                        f"Вы можете войти в {sub_loc.get_description()} (введите 'enter {sub_loc.id}')"
                    )

    def enter_matrix(self, matrix_sub: MatrixSub):
        print(f"Вы вошли в {matrix_sub.get_description()}")
        while True:
            command = input("Введите команду (north, south, east, west, exit): ")
            if command in [
                Direction.NORTH,
                Direction.SOUTH,
                Direction.EAST,
                Direction.WEST,
            ]:
                matrix_sub.move(command)
            elif command == "exit":
                print(f"Вы вышли из {matrix_sub.get_description()}")
                return
            else:
                print("Неверная команда.")


def load_map():
    try:
        conn = sqlite3.connect("game_map.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS locations (
                id TEXT PRIMARY KEY,
                description TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS connections (
                from_location TEXT,
                direction TEXT,
                to_location TEXT,
                FOREIGN KEY (from_location) REFERENCES locations (id),
                FOREIGN KEY (to_location) REFERENCES locations (id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sub_locations (
                id TEXT PRIMARY KEY,
                description TEXT,
                parent_location TEXT,
                FOREIGN KEY (parent_location) REFERENCES locations (id)
            )
        """
        )

        locations = [
            ("start", "Вы находитесь в НАЧАЛЕ ПУТИ."),
            ("north_location", "Вы находитесь в СЕВЕРНОЙ ЛОКАЦИИ."),
            ("south_location", "Вы находитесь в ЮЖНОЙ ЛОКАЦИИ."),
            ("east_location", "Вы находитесь в ВОСТОЧНОЙ ЛОКАЦИИ."),
            ("west_location", "Вы находитесь в ЗАПАДНОЙ ЛОКАЦИИ."),
            ("sub_north_1", "Вы находитесь В Первой части СЕВЕРА."),
            ("sub_north_2", "Вы находитесь во Второй части СЕВЕРА."),
            ("sub_north_3", "Вы находитесь в Третьей части СЕВЕРА."),
            ("sub_south_1", "Вы находитесь в Первой части ЮГА"),
            ("sub_south_2", "Вы находитесь во Второй части ЮГА"),
            ("sub_south_3", "Вы находитесь в Третьей части ЮГА"),
            ("sub_east_1", "Вы находитесь в Первой части ВОСТОКА"),
            ("sub_east_2", "Вы находитесь во Второй части ВОСТОКА"),
            ("sub_east_3", "Вы находитесь в Третьей части ВОСТОКА"),
            ("sub_west_1", "Вы находитесь в Первой части ЗАПАДА"),
            ("sub_west_2", "Вы находитесь во Второй части ЗАПАДА"),
            ("sub_west_3", "Вы находитеь в Третьей части ЗАПАДА"),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO locations (id, description) VALUES (?, ?)", locations
        )

        connections = [
            ("start", Direction.NORTH, "north_location"),
            ("start", Direction.SOUTH, "south_location"),
            ("start", Direction.EAST, "east_location"),
            ("start", Direction.WEST, "west_location"),
            ("north_location", Direction.SOUTH, "start"),
            ("south_location", Direction.NORTH, "start"),
            ("east_location", Direction.WEST, "start"),
            ("west_location", Direction.EAST, "start"),
        ]

        cursor.executemany(
            "INSERT INTO connections (from_location, direction, to_location) VALUES (?, ?, ?)",
            connections,
        )

        sub_locations = [
            ("sub_north_1", "Первая часть СЕВЕРА.", "north_location"),
            ("sub_north_2", "Вторая часть СЕВЕРА.", "north_location"),
            ("sub_north_3", "Третья часть СЕВЕРА.", "north_location"),
            ("sub_south_1", "Первая часть ЮГА.", "south_location"),
            ("sub_south_2", "Вторая часть ЮГА.", "south_location"),
            ("sub_south_3", "Третья часть ЮГА.", "south_location"),
            ("sub_east_1", "Первая часть ВОСТОКА.", "east_location"),
            ("sub_east_2", "Вторая часть ВОСТОКА.", "east_location"),
            ("sub_east_3", "Третья часть ВОСТОКА.", "east_location"),
            ("sub_west_1", "Первая часть ЗАПАДА.", "west_location"),
            ("sub_west_2", "Вторая часть ЗАПАДА.", "west_location"),
            ("sub_west_3", "Третья часть ЗАПАДА.", "west_location"),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO sub_locations (id, description, parent_location) VALUES (?, ?, ?)",
            sub_locations,
        )

        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Ошибка при подключении к базе. {e}")


def main():
    load_map()

    conn = sqlite3.connect("game_map.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM locations")
    location_data = cursor.fetchall()

    locations = {}
    for loc in location_data:
        loc_id, description = loc
        locations[loc_id] = Location(loc_id, description)

    cursor.execute("SELECT * FROM connections")
    connections_data = cursor.fetchall()
    for from_loc, direction, to_loc in connections_data:
        locations[from_loc].connect(direction, locations[to_loc])

    cursor.execute("SELECT * FROM sub_locations")
    sub_locations = cursor.fetchall()
    for sub_loc_id, sub_description, parent_loc in sub_locations:
        all_subloc = {
            "sub_north_1",
            "sub_north_2",
            "sub_north_3",
            "sub_south_1",
            "sub_south_2",
            "sub_south_3",
            "sub_east_1",
            "sub_east_2",
            "sub_east_3",
            "sub_west_1",
            "sub_west_2",
            "sub_west_3",
        }
        if sub_loc_id in all_subloc:
            sub_location = MatrixSub(sub_loc_id, sub_description)
        else:
            sub_location = SubLocation(sub_loc_id, sub_description)
        locations[parent_loc].add_sub_location(sub_location)

    conn.close()

    protagonist = Protagonist(
        name="name", id="player", start_location=locations["start"]
    )
    protagonist.display_current_location()
    while True:
        command = input(
            "Введите команду (go [north/south/east/west], enter[sub_loc_1/sub_loc_2/sub_loc_3], exit): "
        )
        if command.startswith("go "):
            direction = command.split()[1]
            protagonist.go(direction)
        elif command.startswith("enter "):
            sub_loc_id = command.split()[1]
            sub_location = protagonist.current_location.get_sub_location().get(
                sub_loc_id
            )
            if isinstance(sub_location, MatrixSub):
                protagonist.enter_matrix(sub_location)
            else:
                print("Эта подлокация не доступна")
        elif command == "exit":
            print("Вы вышли из игры.")
            break
        else:
            print("Неверная команда")


if __name__ == "__main__":
    main()
