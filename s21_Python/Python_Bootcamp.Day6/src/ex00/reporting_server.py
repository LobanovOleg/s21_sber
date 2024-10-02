import grpc
from concurrent import futures
import random
import space_ship_pb2
import space_ship_pb2_grpc

names = ("Leonardo", "Rafael", "Donatello", "Michelangelo", "Splinter", "April")
surnames = ("Da Vinchi", "Santi", "Bardi", "Simoni", "Rat", "O`Neal")
ranks = ("Captain", "Sergeant", "Admiral", "Lieutenant", "Commander")

enemies_straship = ("Executor", "Unknown", "Emperial Destroyer", "Star Shuttle")
ally_starship = ("Falcon", "Normandy", "X-Wing")


def stat_officer():
    return {
        "first_name": random.choice(names),
        "last_name": random.choice(surnames),
        "rank": random.choice(ranks),
    }


def ship_init():
    ship = space_ship_pb2.SpaceShip()
    ship.alignment = random.randint(1, 2)
    if ship.alignment == 2:
        ship.name = random.choice(enemies_straship)
        officers_number = random.randint(1, 10)
    elif ship.alignment == 1:
        ship.name = random.choice(ally_starship)
        officers_number = random.randint(1, 10)
    ship.ship_class = random.randint(0, 5)
    ship.length = round(random.uniform(80.0, 2000.0), 1)
    ship.crew_size = random.randint(4, 500)
    ship.armed = random.randint(0, 1)
    result = {
        "alignment": ship.alignment,
        "name": ship.name,
        "ship_class": ship.ship_class,
        "length": ship.length,
        "crew_size": ship.crew_size,
        "armed": ship.armed,
        "officers": [stat_officer() for _ in range(officers_number)],
    }
    return result


class Service(space_ship_pb2_grpc.UnaryServicer):
    def GetServerResponse(self, request, context):
        ships = [
            space_ship_pb2.SpaceShip(**ship_init())
            for _ in range(random.randint(1, 10))
        ]
        yield from ships


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    space_ship_pb2_grpc.add_UnaryServicer_to_server(Service(), server)
    server.add_insecure_port("[::]:8888")
    server.start()
    print("Server Started")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
