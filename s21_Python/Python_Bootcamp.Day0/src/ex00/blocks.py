import sys

if len(sys.argv) < 2:
    print("Введите количество строк в качестве первого аргумента командной строки")
    sys.exit()

num = int(sys.argv[1])
for _ in range(num):
    line = input()
    if len(line) == 32 and line[:5] == "00000" and line[5] != "0":
        print(line)
