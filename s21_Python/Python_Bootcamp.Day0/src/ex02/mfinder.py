str = ""
for _ in range(3):
    str += input()

m = [0, 4, 5, 6, 8, 9, 10, 12, 14]
err = "True"

if len(str) != 15:
    err = "Error"
else:
    for i in range(15):
        if i in m and str[i] != "*":
            err = "False"
        if i not in m and str[i] == "*":
            err = "False"
print(err)
