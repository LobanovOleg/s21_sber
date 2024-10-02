# Day 08 — Python Bootcamp

## Temet Nosce

💡 [Tap here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) **to leave your feedback on the project**. It's anonymous and will help our team make your educational experience better. We recommend completing the survey immediately after the project.

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: I Know Kung Fu](#exercise-00-i-know-kung-fu)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: A Squid On A Stick](#exercise-01-a-squid-on-a-stick)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: DejaVu](#exercise-02-deja-vu)

## Chapter I
### General rules

- Your scripts should not exit unexpectedly (return an error on valid input). If this happens, your project will be considered non-functional and will receive a 0 in the evaluation.
- Submit your work to your assigned git repository. Only the work in the git repository will be evaluated.

## Chapter II
### Rules of the day

- You should turn in `*.py` and `requirements.txt` files for this task.

## Chapter III
### Intro

Seraph took a small sip from his teacup.

 "You are the One. And your enemy is also one, but many."
 
 "Is this a riddle?" Neo sank onto the nearest bench.
 
 "No. But you must practice fighting several enemies at once."
 
 "I've done that, several times. You just knock out one, then the other..."
 
Seraph raised his hand in a reassuring gesture. "You know that real enemies will almost never attack you one by one?"
 
 "Of course. This is not a movie. Just a virtual reality."
 
 "The pause between moves can be a split second. You have to keep track of your surroundings and switch between appropriate counter-actions."
 
Neo took a sip as well. Even though he knew that the tea was a total fiction, this Da Hong Pao was amazing.

## Chapter IV
### Exercise 00: I Know Kung Fu

The good thing about the Matrix is that everything can be simulated. Every situation within the system is just a program written by a human or machine for a specific purpose.

This is why Nebuchadnezzar's operator was able to see the actual images behind the green letters on the screen. As Neo and Seraph discussed the training, the code began to look like this:

```python
import asyncio

from enum import Enum, auto
from random import choice


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)
```

For the sake of simplicity, there are only four actions available to both the Agent and Neo in this training session. The recipe for winning a fight is simple: for each kick, Neo must protect the part (high/low) where the Agent is aiming, and for each block, the Agent must target an unblocked part of the body.

You will need to write a script called "fight.py", which will contain the unmodified code from above, but also an asynchronous function "fight()", which will implement the logic explained above.

The output of the script might look like this (since the actions are randomized, the actual result will be different each time):
 
```
Agent: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent Health: 4
Agent: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent Health: 3
Agent: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent Health: 3
Agent: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent Health: 3
Agent: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent Health: 2
Agent: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent Health: 2
Agent: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent Health: 2
Agent: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent Health: 2
Agent: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent Health: 1
Agent: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent Health: 0
Neo wins!
```

BONUS: for additional points you can write another function called 'fightmany(n)', where instead of one agent Neo will fight a number (a list) of them, so the first line could be:

`agents = [Agent() for _ in range(n)]`

Try to find a way to randomize incoming actions from agents and respond to them appropriately. The battle with three Agents log might look like this:

```
Agent 1: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 1 Health: 4
Agent 2: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 2 Health: 5
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 4
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 3
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 4
Agent 1: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 1 Health: 4
Agent 2: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 2 Health: 4
Agent 1: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 1 Health: 3
Agent 3: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 3 Health: 3
Agent 3: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 3 Health: 3
Agent 3: Action.LOWKICK, Neo: Action.LOWBLOCK, Agent 3 Health: 3
Agent 1: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent 1 Health: 3
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 3
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 2
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 2
Agent 2: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent 2 Health: 2
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 1
Agent 1: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 1 Health: 2
Agent 1: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 1 Health: 1
Agent 2: Action.HIGHKICK, Neo: Action.HIGHBLOCK, Agent 2 Health: 2
Agent 3: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 3 Health: 0
Agent 2: Action.LOWBLOCK, Neo: Action.HIGHKICK, Agent 2 Health: 1
Agent 1: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 1 Health: 0
Agent 2: Action.HIGHBLOCK, Neo: Action.LOWKICK, Agent 2 Health: 0
Neo wins!
```

## Chapter V
### Exercise 01: A Squid On A Stick

As a program, Seraph dedicated his existence to serving and protecting the Oracle. But one of the most valuable lessons he taught Neo had nothing to do with martial arts.

The Matrix is an artificial world. Every interaction within it is not a real kick in the teeth, but a bunch of bytes sent over the network connection. And the entire history of network communication for mankind is a contest between attackers and defenders.

And one of the primary weapons in that battle is tracking. Agents track hackers who connect to the Matrix from the outside. Squiddies search for members of the resistance. Matrix runners look for the rogue programs that might agree to become invaluable insider agents.

So let's build a crawler.

Let's be minimalist for this task. The program should consist of two files - `crawl.py` and `server.py`. It is recommended to use [aiohttp](https://docs.aiohttp.org/en/stable/) or [httpx](https://www.python-httpx.org/) for the client side and [FastAPI](https://fastapi.tiangolo.com/) for the server side. All I/O code should be asynchronous.

The workflow is as follows:
- Server is started and listens on port 8888.
- Client (`crawl.py`) gets one or more queryable URLs as argument.
- Client submits all URLs via HTTP POST request as a JSON list to a server endpoint `/api/v1/tasks/`.
- Server responds with HTTP 201 created and a task object (consider using [PyDantic](https://pydantic-docs.helpmanual.io/)).
- Task object contains status "running" and ID, which is [UUID4](https://docs.python.org/3/library/uuid.html#uuid.uuid4).
- server then starts asynchronously (don't use threads or multiprocessing) sending HTTP GET requests to submitted URLs and collecting HTTP response codes, whether it's 200, 404 or some other - client keeps periodically querying endpoint `/api/v1/tasks/{received_task_id}` until server finishes processing all URLs. Then the task status should change to "ready" and the task's "result" field should contain a list of HTTP response codes for the submitted URLs.
- Client prints tab-separated HTTP response code and corresponding URL for each entry.

In the synchronous world, people often implement this using modules like [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html), but in this task no external workers are needed, so the whole server should be in a single Python file, and all the code should use the [async/await paradigm](https://docs.python.org/3/library/asyncio-task.html).

## Chapter VI
### Exercise 02: Deja Vu

 "Whenever you see the same event repeated twice, it means it's time to prepare for the worst."
 
Neo thought about it for a moment, but then it dawned on him what Seraph meant.

 "Déjà vu is a glitch in the Matrix, right?"
 
 "It's more like a sigh of sudden change in the environment."
 
 "So what are my options in this case?"
 
 "Escape, of course. There is no shame in that. But it also helps to keep track of the
 objects also helps."
 
 "In what way?"
 
 "If they are part of the déjà vu, it means they were not changed during the upgrade."
 
Neo wanted to ask more questions, but Seraph closed his eyes and politely led him to the door behind him. The Oracle was waiting.

-----

One of the features our crawler still lacks is caching. If the server has seen one of the submitted URLs recently, it can just take the cached value for an HTTP code.

Another thing would be to collect some metrics on the input data. Regardless of whether the URL was cached or not, let's also count on a server how many requests we've done so far for a particular domain (e.g. for "https://www.google.com/search?q=there+is+no+spoon" the domain would be "www.google.com").

You should use Redis for both the cache counter and the domain counter. All code should still be asynchronous, using the async/await paradigm. You may consider using the [redis](https://github.com/redis/redis-py) library for this task. Since the client code is not affected, you should only submit a file with a modified EX01 server code called "server_cached.py".

BONUS: Update your code to include another coroutine that cleans up the cached entries after a configurable timeout.

