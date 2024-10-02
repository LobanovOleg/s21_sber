from wsgiref.simple_server import make_server
from urllib.parse import parse_qs


unknown = "Unknown"

list_of_species = {
    "Cyberman": "John Lumic",
    "Dalek": "Davros",
    "Judoon": "Shadow Proclamation Convetion 15 Enforcer",
    "Human": "Leonardo da Vinci",
    "Ood": "Klineman Halpen",
    "Silence": "Tasha Lem",
    "Slitheen": "Coca-Cola salesman",
    "Sontaran": "General Staal",
    "Time Lord": "Rassilon",
    "Weeping Angel": "The Division Representative",
    "Zygon": "Broton",
    unknown: unknown,
}


def application(environ, start_response):
    d = parse_qs(environ["QUERY_STRING"])
    species = d.get("species", [unknown])[0]
    name = list_of_species.get(species, unknown)

    response_body = f'{{"credentials" : "{name}"}}\n'.encode("UTF-8")
    status = '200 OK' if name != unknown else '404 Not found'
    response_headers = [
        ("Content-Type", "text/plain; charset=utf-8"),
        ("Content-Length", str(len(response_body))),
    ]
    start_response(status, response_headers)
    return [response_body]


def main():
    server = make_server("localhost", 8888, application)
    print(f"Serving HTTP on port 8888...")
    server.serve_forever()


if __name__ == "__main__":
    main()
