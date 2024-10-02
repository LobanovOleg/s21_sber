import ex00_ingot

print()
purse_10: dict[str, int] = {"gold_ingots": 10}
print("\t" + "Tests purse 10")
print("add test")
print(ex00_ingot.add_ingot(purse_10))
print()
print("get test")
print(ex00_ingot.get_ingot(purse_10))
print()
print("empty test")
print(ex00_ingot.empty(purse_10))

print()
purse_gold_rock: dict[str, int] = {"gold_ingots": 10, "rock": 5}
print("\t" + "Tests purse and rocks")
print("add test")
print(ex00_ingot.add_ingot(purse_gold_rock))
print()
print("get test")
print(ex00_ingot.get_ingot(purse_gold_rock))
print()
print("empty")
print(ex00_ingot.empty(purse_gold_rock))

print()
purse_empty: dict[str, int] = {}
print("\t" + "Tests empty")
print("add test")
print(ex00_ingot.add_ingot(purse_empty))
print()
print("get test")
print(ex00_ingot.get_ingot(purse_empty))
print()
print("empty test")
print(ex00_ingot.empty(purse_empty))
