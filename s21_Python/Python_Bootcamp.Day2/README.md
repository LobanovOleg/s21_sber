# Day 02 — Python Bootcamp

## Vault 26

Discover the mysteries of a closed Vault!

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Gaining Access](#exercise-00-gaining-access)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Morality](#exercise-01-morality)
6. [Chapter VI](#chapter-vi) \
    6.1. [Reading and tips](#reading-and-tips)

## Chapter I
### General rules

- Your scripts should not exit unexpectedly (return an error on valid input). If this happens, your project will be considered non-functional and will receive a 0 in the evaluation.
- We encourage you to create test programs for your project, even though this work doesn't have to be submitted and won't be graded. This will allow you to easily test your work and the work of your peers. You will find these tests particularly useful during your defense. In fact, you are free to use your tests and/or the tests of the peer you are evaluating during your defense.
- Submit your work to your assigned git repository. Only work in the git repository will be graded.
- It is recommended that you have Python version 3.7+ (and definitely NOT <3.4). You can manage different interpreter versions with [pyenv] (https://github.com/pyenv/pyenv).
- It is recommended (though not required) that your code is formatted according to the [PEP8 style guides](https://peps.python.org/pep-0008/) (modern IDEs can check this automatically). For a short tutorial, see [this article](https://realpython.com/python-pep8/).
- It is also recommended (though not required) that you use type hinting in your code. For a short tutorial, see [this article](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).

## Chapter II
### Rules of the day

- You should only submit `*.py` files.
- It is also recommended to write some tests for different cases inside your scripts. To make them run only when the script is executed directly and not imported from somewhere else, you can use the `if __name__ == "__main__":` statement. You can read more about this [here](https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/).
- You can guess (or model) the solution to EX01, or you can go through [this little tutorial on game theory](https://ncase.me/trust/) to help you with that.

## Chapter III
### Intro

The Chosen One stood before a massive doorway, well hidden in an
underground cavern that stretched deep into the mountain. A closed door, especially one that has not been opened for more than a hundred years, definitely holds a secret. It can be dark and sad, or it can be fun and adventurous. These guys might even have a spare GECK!

But our hero's attention was drawn to the console next to the door. He approached it slowly, watching his steps carefully, just in case. Then he pulled an electronic lockpick (made by Wattz Electronics, Mk2!) out of his pocket and plugged it into a slot on the side.

The screen lit up and the Chosen One sighed with relief — at least the vault's reactor was online and this thing still had power. This could work.

But instead of the usual hex dump where he could search for the password, it showed something completely unexpected — a series of lines appeared on the screen:

```
AssertionError: len(key) == 1337
AssertionError: key[404] == 3
AssertionError: key > 9000
AssertionError: key.passphrase == "zax2rulez"
AssertionError: str(key) == "GeneralTsoKeycard"

```

Okay, right, the lockpick is programmable. But what the hell is with this
error?


## Chapter IV
### Exercise 00: Gaining Access

Our hero put his backpack on the ground and took out a thick book called "Dean's Electronics". It was mostly about hardware, but there was a whole section on programming. He read that "assert" is a special statement whose sole purpose is to check whether a certain condition is met. Apparently, in this case, the system expected the inserted digital key to pass several checks before opening the door.

But it was still strange. The first two lines implied that 'key' was a list, but then comparing it to number 9000 completely ruined that assumption. Looks like a custom data type had to be introduced.

In the last chapter, the book also mentioned that custom types can be introduced using classes. There was one more thing though — a lockpick he had had a very tiny memory and couldn't really hold 1337 elements in it, even worse, it couldn't hold 404 either. Was there a way around it?

The last page in this chapter had been torn and lost decades ago, only a small piece was left. It only had one line that looked like this:

`__magic_methods__`

with double underscores on both sides.

The Chosen One thought about this for a full five minutes, then plugged the lockpick into his trusty PipBoy and started coding.

-----

You need to describe a Python class `Key' so that an instance of this class would pass the checks listed above. Note that your code in this exercise shouldn't create containers of size 404 or smaller. Even without them, you should be able to pass these checks.

You are encouraged to write an actual set of tests to simulate the key checks according to the bugs above (and to make peer review easier). This will be graded as a bonus.

## Chapter V
### Exercise 01: Morality

Finally, the massive door began to open! Just in case, the Chosen One put his hand on the holster. Last time, opening a door like this had led to a long shootout with ghouls.

But the room behind the door was empty. And clean. In fact, there wasn't much room at all — just a small room with a terminal and no way deeper into the vault. 

The screen of a terminal lit up, showing a logo of something called "ZAX 2.0", and a strange synthetic voice echoed through the room.

 "Greetings, visitor! I see the war is over and now it's my turn to take over!"

Our hero was stunned for a moment, but this wasn't the first time he encountered a sophisticated security system.

 "Hello, what do you mean "take over"?"

 "My name is ZAX, and I was created to restore humanity to its glory when the bad times are over! Welcome human, now let's restore the world to its glory!"

...After about an hour of discussion, the picture began to come together. ZAX was created by some brilliant scientists long before the war to solve the problems of distributing limited resources. When the fallout came on the horizon, it was reprogrammed based on the same principles to "rule the world", which meant "provide optimizations for supply chains". Basically, the whole vault was just one big computer.

The AI started asking the Chosen One a lot of questions about what was going on on the surface, and also how long it would take to get the current "big shots" here, into the vault, so he could start his "life's work".

 "I am currently working through what you humans call the 'prisoner's dilemma'," ZAX admitted. "During my time here, based on all the information I had, I started classifying people by their behavior."

ZAX told of the simple game of candy, where there is a machine that controls the supply of candy to two groups of people based on whether one or both of two operators put candy in it:

|  | Both cooperate | 1 cheats, 2 cooperates | 1 cooperates, 2 cheats | Both cheat |
|------------|----------|----------|----------|---------|
| Operator 1 | +2 candy | +3 candy | -1 candy | 0 candy |
| Operator 2 | +2 candy | -1 candy | +3 candy | 0 candy |

So if everyone cooperates and puts candy into the machine as agreed, everyone gets a reward. But both participants also have the temptation to cheat and only pretend to put a candy into the machine, because in this case their group will get 3 candies back by taking only one candy from a second group. The problem is that if both operators decide to play dirty, then nobody gets anything.

ZAX also mentioned five behavioral models that he used to run experiments:

| Behavior type | Player Actions                                                                                                                                                                                         |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Cheater       | Always cheats                                                                                                                                                                                          |
| Cooperator    | Always cooperates                                                                                                                                                                                      |
| Copycat       | Starts with cooperating, but then just repeats whatever the other guy is doing                                                                                                                         |
| Grudger       | Starts by always cooperating, but switches to Cheater forever if another guy cheats even once                                                                                                          |
| Detective     | First four times goes with [Cooperate, Cheat, Cooperate, Cooperate],  and if during these four turns another guy cheats even once — switches into a Copycat. Otherwise, switches into Cheater himself |

-----

To finish the experiment with ZAX, you need to model a system with seven classes — `Game`, `Player` and five behavior types (subclassed from `Player`).

The skeleton for a `Game` class looks like this:

```python
from collections import Counter

class Game(object):

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1, player2):
        # simulate number of matches
        # equal to self.matches

    def top3(self):
        # print top three
```

Here `registry` is used to keep track of the current number of candies during the game, while `player1` and `player2` are instances of subclasses of `Player` (each being one of 5 behavior types). Calling the `play()` method of a `Game` instance should simulate a given number of games between players of a given behavior.

The `top3()` method should print the current top three players' behaviors along with their current score, such as:

```
cheater 10
detective 9
grudger 8
```

By default, your code, when run, should simulate 10 games (one call to `play()`) between each pair of two players with *different* behavior types (a total of 10 rounds of 10 games each, no games between two copies of the same behavior), and print the top three winners after the entire game.

You are strongly encouraged to experiment with different behaviors and write your own class of behaviors (this will be scored as a bonus). You can get even more bonus points if an instance of your class outperforms at least three out of five provided behaviors in the same "competition between each pair of players" check.

Don't forget that the only thing a player can do each turn is either cooperate or cheat, based on the history of the current game.

-----

...A few hours later, the Chosen One left the vault with ZAX, closing the door behind him. He got what he wanted — a whole new set of interesting thoughts to wrap his head around. And about ruling the world... in its current state, the world wasn't ready for something like ZAX. Not like wild robbers would ever give the crown to a tin can. Not like the Chosen One himself.

## Chapter VI
### Reading and tips

Classes in Python fully support inheritance, but do not provide encapsulation very well. Probably one of the most interesting things to look at in Python OOP is `super()`, you can read about it [e.g. here](https://realpython.com/python-super/).

Another thing to read about is a "constructor", which in Python is complex and includes at least two methods — `__new__` and `__init__`. Here is [some more information](https://medium.com/thedevproject/new-vs-init-in-python-a-most-known-resource-7beb538dc3b) on this topic.   

**Please leave your feedback [here](https://forms.gle/oMEJnwqt5pkLydYy5)**
