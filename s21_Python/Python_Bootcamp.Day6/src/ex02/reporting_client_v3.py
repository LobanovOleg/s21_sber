import grpc
import psycopg2
import space_ship_pb2
import space_ship_pb2_grpc
import sys


def get_spaceships_from_generator():
    channel = grpc.insecure_channel("localhost:8888")
    stub = space_ship_pb2_grpc.UnaryStub(channel)

    response = stub.GetServerResponse(space_ship_pb2.Message())
    spaceships = [ship for ship in response]

    return spaceships


class ReportingClient:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="db_for_ship", user="lowban", host="localhost"
        )
        self.cur = self.conn.cursor()

    def scan_and_save_to_db(self):
        spaceships = get_spaceships_from_generator()

        for ship in spaceships:
            self.cur.execute(
                "INSERT INTO ships (ship_name, alignment, latitude_h, latitude_m, latitude_s, longitude_h, longitude_m, longitude_s) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING ship_id",
                (
                    ship.name,
                    ship.alignment,
                    sys.argv[1],
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                    sys.argv[5],
                    sys.argv[6],
                ),
            )
            ship_id = self.cur.fetchone()[0]

            for officer in ship.officers:
                self.cur.execute(
                    "INSERT INTO crew_members (ship_id, ship_name, alignment, first_name, last_name, rank) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        ship_id,
                        ship.name,
                        ship.alignment,
                        officer.first_name,
                        officer.last_name,
                        officer.rank,
                    ),
                )

        self.conn.commit()

    def scan(self):
        self.cur.execute(
            "SELECT DISTINCT c1.first_name, c1.last_name, c1.rank, c1.alignment FROM crew_members c1 JOIN crew_members c2 ON c1.first_name = c2.first_name AND c1.last_name = c2.last_name AND c1.rank = c2.rank AND c1.alignment != c2.alignment"
        )
        traitors = self.cur.fetchall()

        for traitor in traitors:
            self.cur.execute(
                "SELECT COUNT(*) FROM list_traitors WHERE first_name = %s AND last_name = %s AND rank = %s",
                (traitor[0], traitor[1], traitor[2]),
            )
            count = self.cur.fetchone()[0]

            if count == 0:
                self.cur.execute(
                    "INSERT INTO list_traitors (first_name, last_name, rank) VALUES (%s, %s, %s)",
                    (traitor[0], traitor[1], traitor[2]),
                )

        self.conn.commit()

    def list_traitors(self):
        self.cur.execute("SELECT first_name, last_name, rank FROM list_traitors")
        traitors = self.cur.fetchall()

        for traitor in traitors:
            print(
                {"first_name": traitor[0], "last_name": traitor[1], "rank": traitor[2]}
            )


def main():
    client = ReportingClient()

    if sys.argv[1] == "scan":
        client.scan()
    elif sys.argv[1] == "list_traitors":
        client.list_traitors()
    else:
        client.scan_and_save_to_db()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
