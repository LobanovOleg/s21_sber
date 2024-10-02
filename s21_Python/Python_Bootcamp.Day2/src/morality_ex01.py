from collections import Counter
import random


class Game(object):
    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1, player2):
        history = {"player1": [], "player2": []}
        self.registry[player1.name] = self.registry.get(player1.name, 0)
        self.registry[player2.name] = self.registry.get(player2.name, 0)
        for match in range(self.matches):
            first = player1.choose(history["player2"])
            second = player2.choose(history["player1"])
            if first:
                if second:
                    self.registry[player1.name] += 2
                    self.registry[player2.name] += 2
                else:
                    self.registry[player1.name] -= 1
                    self.registry[player2.name] += 3
            elif second:
                self.registry[player1.name] += 3
                self.registry[player2.name] -= 1
            else:
                self.registry[player1.name] += 0
                self.registry[player1.name] += 0
            history["player1"].append(first)
            history["player2"].append(second)

    def top3(self):
        for top in self.registry.most_common(3):
            print(top[0], top[1])

    def classic_play(self, players, clear=False):
        if clear:
            self.registry = Counter()
        for n, player1 in enumerate(players):
            for player2 in players[n + 1 :]:
                self.play(player1, player2)
        self.top3()


class Player:
    def __init__(self, name="random_player"):
        self.name = name

    def choose(self, history):
        return random.choice([True, False])


class Cheater(Player):
    def __init__(self):
        super().__init__(name="cheater")

    def choose(self, history):
        return False


class Cooperator(Player):
    def __init__(self):
        super().__init__(name="cooperator")

    def choose(self, history):
        return True


class Copycat(Player):
    def __init__(self):
        super().__init__(name="copycat")

    def choose(self, history):
        if not history:
            return True
        elif history[-1] == False:
            return False
        else:
            return True


class Grudger(Player):
    def __init__(self):
        super().__init__(name="grudger")

    def choose(self, history):
        if False in history:
            return False
        else:
            return True


class Detective(Player):
    def __init__(self):
        super().__init__(name="detective")

    def choose(self, history):
        quantity = len(history)
        if not history or quantity in (0, 2, 3):
            return True
        elif quantity == 1:
            return False
        elif False in history[:4]:
            return history[-1]
        return False


class Copykitten(Player):
    def __init__(self):
        super().__init__(name="copykitten")

    def choose(self, history):
        if len(history) > 1 and history[-1] is False and history[-2] is False:
            return False
        return True


class Simpleton(Player):
    def __init__(self):
        super().__init__(name="simpleton")
        self.last_move = True

    def choose(self, history):
        if not history:
            return True
        elif history[-1] == True:
            return self.last_move
        else:
            self.last_move = not self.last_move
            return self.last_move


if __name__ == "__main__":
    game = Game()
    players = [Cheater(), Cooperator(), Copycat(), Grudger(), Detective()]
    print("=== The first defaultest game: 5x1, 10 matches ===")
    game.classic_play(players)
    print(game.registry)

    print("=== The second defaultest game: 5x1, 100 matches ===")
    game.matches = 100
    game.classic_play(players, clear=True)
    print(game.registry)

    print("=== The third defaultest game: 5x10, 10 matches ===")
    game.matches = 10
    players *= 10
    game.classic_play(players, clear=True)
    print(game.registry)

    print("=== The fours defaultest game: 5x10, mathces 100 ===")
    game.matches = 100
    game.classic_play(players, clear=True)
    print(game.registry)

    print("--------------------------------------------------------------------------")
    game2 = Game()
    players = [Cheater(), Cooperator(), Copycat(), Grudger(), Detective(), Copykitten()]
    print("=== The first game + copykitten: 6x1, 10 matches ===")
    game2.matches = 10
    game2.classic_play(players)
    print(game2.registry)

    print("=== The second game + copykitten: 6x1, 100 matches ===")
    game2.matches = 100
    game2.classic_play(players, clear=True)
    print(game2.registry)

    print("=== The third game + copykitten: 6x10, 10 matches ===")
    game2.matches = 10
    players *= 10
    game2.classic_play(players, clear=True)
    print(game2.registry)

    print("=== The fours game + copykitten: 6x10, 100 matches ===")
    game2.matches = 100
    game2.classic_play(players, clear=True)
    print(game2.registry)

    print("--------------------------------------------------------------------------")
    game3 = Game()
    players = [Cheater(), Cooperator(), Copycat(), Grudger(), Detective(), Simpleton()]
    print("=== The first game + simpleton: 6x1, 10 matches ===")
    game3.matches = 10
    game3.classic_play(players)
    print(game3.registry)

    print("=== The second game + simplton: 6x1, 100 matches ===")
    game3.matches = 100
    game3.classic_play(players, clear=True)
    print(game3.registry)

    print("=== The third game + simpleton: 6x10, 10 matches ===")
    game3.matches = 10
    players *= 10
    game3.classic_play(players, clear=True)
    print(game3.registry)

    print("=== The fours game + simpleton: 6x10, 100 matches ===")
    game3.matches = 100
    game3.classic_play(players, clear=True)
    print(game3.registry)

    print("--------------------------------------------------------------------------")
    game4 = Game()
    players = [
        Cheater(),
        Cooperator(),
        Copycat(),
        Grudger(),
        Detective(),
        Copykitten(),
        Simpleton(),
    ]
    print("=== The first full game: 7x1, 10 matches ===")
    game4.matches = 10
    game4.classic_play(players)
    print(game4.registry)

    print("=== The second full game: 7x1, 100 matches ===")
    game4.matches = 100
    game4.classic_play(players, clear=True)
    print(game4.registry)

    print("=== The third full game: 7x10, 10 matches ===")
    game4.matches = 10
    players *= 10
    game4.classic_play(players, clear=True)
    print(game4.registry)

    print("=== The fours full game: 7x10, 100 matches ===")
    game4.matches = 100
    game4.classic_play(players, clear=True)
    print(game4.registry)
