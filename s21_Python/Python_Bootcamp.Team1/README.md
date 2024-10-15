# Team 01 - Python Bootcamp

## Game Night

💡 [Tap here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) **to leave your feedback on the project**. It's anonymous and will help our team make your educational experience better. We recommend completing the survey immediately after the project.

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Talk and Fight](#exercise-00-talk-and-fight)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: I Like to Move It Move It](#exercise-01-i-like-to-move-it-move-it)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: Don't Shoot the Messenger](#exercise-02-dont-shoot-the-messenger)
7. [Chapter VII](#chapter-vii) \
    7.1. [Exercise 03: The Whole Story](#exercise-03-the-whole-story)

## Chapter I
### General rules

- Your scripts should not exit unexpectedly (return an error on valid input). If this happens, your project will be considered non-functional and will receive a 0 in the evaluation.
- Submit your work to your assigned git repository. Only the work in the git repository will be evaluated.

## Chapter II
### Rules of the day

- You should provide `*.py` and `requirements.txt` (if using external dependencies) files for this task.
- For the database you can use PostgreSQL, Redis or just a JSON file, in any case you should provide some initial data that can be used to bootstrap the game world on another machine.
- In addition, your project should include a set of documentation (guide) that can be generated using Sphinx (you can refer to DAY07 for what it is and how to use it).
- Your project may also include some images (be sure to use royalty-free ones, e.g. from sites like https://www.flaticon.com/).

## Chapter III
### Intro

Hello and welcome to Twenty One Software! We are very excited that your team has decided to pursue a career in game development.

Recent market research shows a growing interest in story-based role-playing games. We are counting on your ability to create a full-featured project from scratch. Such a product usually consists of several pieces that can be developed independently and then combined. Therefore, we strongly encourage your team to divide the work.

There are no restrictions on the universe and setting you can choose. Some examples:

- Wild West (cowboys, natives);
- Fantasy (dwarves, elves, dragons);
- Pirates (treasure, parrots, rum);
- Sci-Fi (aliens, space battles, black holes);
- Cyberpunk (corporations, hacking, ghost in the shell);
- My Little Pony (ponies!).

You're not limited to these examples, so don't let anyone stop you from inventing your own. Feel free to unleash your creativity and good luck!

-----

Here's a skeleton for your main class — the protagonist. Over the course of the day, you'll implement various methods for this class and a few other classes and wrappers.

```python
from collections import defaultdict


class Protagonist:  # you may decide to add some parent class here, e.g. ORM Model
    def __init__(self, name: str, id: str):  # add more parameters if you need
        self.id = id  # a unique identifier of a current player
        self.name: str = name
        self.hp: int = 10
        # replace with self.level = 1  if you decide to use just level
        self.strength: int, self.craft: int = (1, 1)
        # name and count, modify starting inventory at your wish
        self.inventory = defaultdict(int)
        self.inventory["pocket dust"] += 1  # modify starting inventory as you see fit
    
    def talk_to(self, npc: NPC):
        pass  # you'll need to implement this

    def attack(self, enemy: Enemy):
        pass  # you'll need to implement this

    def take_hit(self, value=1):
        self.hp -= value
        if self.hp <= 0:
            # you'll need to catch this exception in your code and handle this endgame 
            # situation properly, e.g. giving player a meaningful message of what 
            # happened and reset the save so he or she can start again  
            raise Exception("You died")
    
    def heal(self, value=1):
        self.strength: int, self.craft: int = (1, 1)  # starting values may differ
        self.hp += 1

    # can be 'advance_level()' instead. Also, are there any situations in your game
    # where a skill is increased by more than one or even decreased?
    def advance_strength(self, value: int = 1):
        self.strength += value

    def advance_craft(self, value: int = 1):
        self.craft += value

    def go(self, direction: Direction):
        pass  # you'll need to implement this in other exercise

    def whereami(self):
        pass  # returns description of the current location

    def take(self, item: str):
        self.inventory[item] += 1

    def give(self, npc: NPC, item: str):
        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            del self.inventory[item]
        npc.receive(item)
```

## Chapter IV
### Exercise 00: Talk and Fight

Since we're designing an RPG, let's focus on skills and actions. To avoid getting overwhelmed with ideas, let's choose one of the two simplest skill leveling systems:

1) Your character starts at level 1. Certain actions within the game can increase the level of the protagonist. A certain level must be reached to perform certain actions. No other explicit abilities are used.
2) Your character doesn't have levels, but instead has a set of two skills - Strength and Craft (this system is used in some popular board games such as [Talisman](https://boardgamegeek.com/boardgame/27627/talisman-revised-4th-edition)).
Certain actions within the game can increase one of these two skills. A certain skill level must be reached in order to perform certain actions.

As you can see in a skeleton above, your character starts with 10 HP (Health Points), which can be increased or decreased depending on the player's actions.

As you can see in the code above, there are at least two more classes to implement:

1) NPC (non-playable character);
2) Enemy (those you have to fight).

If in your game an enemy is a character you can talk to, it might make sense to make `Enemy` a subclass of `NPC`. 

NPCs, Enemies and their initial stats and phrases should be stored in a 
database (can be PostgreSQL, SQLite or just a JSON file on disk). It should be possible to add more phrases to a character just by modifying the database. Note that in this task, all initial parameters for NPCs and enemies should not change during the playthrough, so that all players face the same initial state of the game world. 

The only thing that can change is a player's profile (e.g. level, inventory, location, current dialog line or accepted quests), which is also a savegame. This means that you should design your database structure so that all changes are only related to the `protagonist` profile in the database.  

Another thing to mention is combat. Enemies should also have skills (levels or strength/craft). Let's make the combat mechanic simple: a virtual six-sided die is rolled for both parties, and the resulting number is added to the protagonist's (or enemy's) skill level. If the protagonist's number is greater, the enemy is defeated. If an enemy wins, the protagonist's HP is reduced by one. 

It's up to you whether the current enemy can be attacked again immediately after the player has lost once.

Summary: As a result of this phase, several game classes should be implemented (updated `Protagonist`, also `NPC` and `Enemy`). Please provide a `load_data.py` script that initializes the database with the parameters and phrases for NPCs and enemies, as well as a default player profile with a unique ID.

It should be possible to import these classes, create an instance of a protagonist, and (as long as the initial data is loaded into the database):
- Create instances of specific NPCs from the database and talk to them.
- Exchange items with NPCs (this may only work under certain conditions) — give and take.
- Create instances of specific enemies from the database and fight them.

BONUS: Implement a quest system so that NPCs can give you quests, and if you complete them (bring a certain item, kill a certain monster, or pass the message to another NPC), you will receive a reward or advance in skill. To do this, you'll need to implement more methods on the `Protagonist` and `NPC` classes. 

## Chapter V
### Exercise 01: I Like to Move It Move It

There is one more type in the `Protagonist` skeleton above that is not implemented in other exercises, and that is `Direction`. For the sake of simplicity, let's think of the game world as a collection of interconnected locations, much like these marked squares on a 2d plane:

|   | ⬛ |   |   |   |
|---|---|---|---|---|
| ⬛ | ⬛ |   | ⬛ | ⬛ |
|   | ⬛ | ⬛ | ⬛ |   |
|   |   |   | ⬛ |   |

The point of this exercise is to create a series of interconnected locations where the plot of your game will unfold. Each location should have a short description (don't worry about NPCs and items for now, they can be added later) and a list of directions to other locations.

The whole graph of locations should be represented by a structure in the database (including links connecting adjacent locations). This means that the game world structure should be modifiable without touching the code, just by updating the entries in the database.

Summary: As a result of this phase, code should be written that loads the graph of locations from the database. One of the locations will be marked as the start location, i.e. the player will be spawned there by default at the start of the game. Please provide a script called `load_map.py` that initializes the database with the map of the game locations.

The methods `go()` and `whereami()` should be implemented for a `Protagonist` instance. As a test, it should be possible to "walk around" the game world loaded into the database from the initial data. When a location is entered, a description is loaded from the database and shown to the player (you can just print it in this exercise). 

## Chapter VI
### Exercise 02: Don't Shoot the Messenger

While the previous exercises focused more on game mechanics, this one focuses on an engine. Since the game is turn-based and text-oriented, a good candidate is a Telegram bot.

There are several Python libraries that allow you to interact with the Telegram API. Two of the most popular ones are:

- [telebot](https://github.com/eternnoir/pyTelegramBotAPI);
- [aiogram](https://github.com/aiogram/aiogram).

Choose one of them and with this tool we will focus on one of the most complicated problems in computer science. It's NAMING things.

Your team is probably already discussing the details of characters and items that would be good to have in the game. One point of this exercise is to create a bot with a two-level menu to generate names for different characters and items. 

First, the menu levels. You probably know that Telegram allows the bot to present you with buttons that you can click. Two main buttons on the top level should be named "Characters" and "Items". Feel free to add emoticons to them if you like. After clicking these buttons, the user should be presented with a collection of buttons for various subcategories within a selected category.

For example, for "Characters" it might be "Ponies", "Humans", "Aliens", and "Dwarves". Virtually any class, race, gender, or other subcategory. For "Items" it can be "Weapons", "Potions", "Computer Chips" and "Food". The only requirement is that these categories fall within the narrative of your game. Also, at each menu level deeper than the root, there should be an extra button that allows you to go back to the top level and possibly change your previous choice.

Second, the generation algorithm. The simplest one for characters would be to just make a short list of first and last names and then combine them randomly. However, there are no restrictions and you can implement it in your own way. The same goes for items — you can combine words into something like "Green Magic Sword of Power" or "Rusty Memory Crystal of Hacking".

**IMPORTANT NOTE**: DO NOT share your Telegram Bot token in your submission. Peer reviewers should be able to run your bot themselves by providing their own token. 

_BONUS: Use an asynchronous (async/await) approach._

## Chapter VII
### Exercise 03: The Whole Story

Finally, it's time to put all the pieces together. Set up your game as a Telegram Bot so that the user can move around the world, talk to NPCs, trade items, fight enemies, and advance in skills. This doesn't have to be a long story, but please include all of these mechanics (and optionally quests from the EX00 bonus section) to be present at least once during the story.

The output of this section should not only be a working game as a Telegram Bot, but also a Sphinx-powered documentation with at least two sections, mostly helpful for peer reviewers:

1) How to start the bot yourself.
2) Game walkthrough, which a player can follow from the beginning to the end. 
(or... endings? It's up to you). If you like spoilers, of course.

Also, so as not to spoil anyone's fun, try to verify that it is indeed possible to finish the game without the walkthrough and any prior knowledge. 

Please also provide a `load_all.py` script that initializes the database and populates it with game data (locations, NPC dialog and stats, etc.). 

