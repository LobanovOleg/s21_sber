import grpc
import argparse
import space_ship_pb2
import space_ship_pb2_grpc

from google.protobuf.json_format import MessageToJson
from space_ship import Ship


class Client:
    def __init__(self, host="localhost", port="8888"):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = space_ship_pb2_grpc.UnaryStub(self.channel)

    def response(self, *coords):
        response = {
            "latitude_h": int(coords[0]),
            "latitude_m": int(coords[1]),
            "latitude_s": float(coords[2]),
            "longitude_h": int(coords[3]),
            "longitude_m": int(coords[4]),
            "longitude_s": float(coords[5]),
        }
        message = self.stub.GetServerResponse(space_ship_pb2.Message(**response))
        for msg in message:
            msg_json = MessageToJson(msg, preserving_proto_field_name=True)
            try:
                Ship.parse_raw(msg_json)
                print(msg_json)
            except ValueError as e:
                print(repr(e.errors()[0]["type"]))


def main():
    parser = argparse.ArgumentParser(description="grpc client")
    parser.add_argument("latitude_h", type=int, help="latitude_h")
    parser.add_argument("latitude_m", type=int, help="latitude_m")
    parser.add_argument("latitude_s", type=float, help="latitude_s")
    parser.add_argument("longitude_h", type=int, help="longitude_h")
    parser.add_argument("longitude_m", type=int, help="longitude_m")
    parser.add_argument("longitude_s", type=float, help="longitude_s")
    args = parser.parse_args()
    client = Client()
    client.response(
        args.latitude_h,
        args.latitude_m,
        args.latitude_s,
        args.longitude_h,
        args.longitude_m,
        args.longitude_s,
    )


if __name__ == "__main__":
    main()