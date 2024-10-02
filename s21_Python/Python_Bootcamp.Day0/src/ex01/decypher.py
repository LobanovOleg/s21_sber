import argparse

parser = argparse.ArgumentParser(description="decypher")
parser.add_argument("string", type=str, help="decypher words")
args = parser.parse_args()
words = args.string.split(" ")

decypher = ""
for word in words:
    decypher += word[0]
print(decypher)
