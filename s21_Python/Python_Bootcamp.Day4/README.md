# Day 04 - Python Bootcamp

## The cake is not a lie

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Energy Flow](#exercise-00-energy-flow)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Personalities](#exercise-01-personalities)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: Backpressure](#exercise-02-backpressure)
7. [Chapter VII](#chapter-vii) \
    7.1. [Reading and tips](#reading-and-tips)

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

## Chapter III
### Intro

This was a triumph. Or so Chell thought for a moment when she saw the surface. But later, as she sat in a storage room eating a cake, she wasn't very surprised when the robot arm drew the words "HUGE SUCCESS" with a marker on a whiteboard.

 "I bet you feel very proud of yourself," came the voice from one of the personality cores. on a shelf. "Feel free to enjoy your cake. For now. But then we have some repairs to make."

Chell sighed. She took the core and threw it as far as she could into the darkness.

 "Physiological parameters are normal," another core from the top shelf said immediately. shelf. "Resuming experiments is recommended."

The door on the other side of the storage room suddenly opened, revealing a corridor that seemed to lead to another test chamber. But at the same time, the robotic hand tried to grab the portal weapon. Chell quickly jumped aside and gave the security camera on one wall a very angry look.

 "No need for strong emotions. The Aperture Science Handheld Portal Device will not be necessary for these next tasks. You may keep it if you wish," the voice was as impassive as ever. "Please proceed to the Production Center."

Chell hesitated a bit, then shrugged, apparently coming to a conclusion. Then she took the next powered personality core from the shelf and went through the door.

## Chapter IV
### Exercise 00: Energy Flow

The room turned out to be quite small. One wall had a large window with a dark area behind it. Chell's eyes widened in surprise when she realized that this was actually a monitoring room for the test chamber. From the other side.

 "Due to mandatory scheduled maintenance, the appropriate chamber for this test is currently unavailable. Due to a lack of personnel, an exception has been made and a test subject is required to perform the maintenance," GLaDOS said from the core.

A service manual lay on the table. Chell quickly scanned it. Most repairs were supposed to be done by specialized robots, but an AI that guided them went offline after GLaDOS' main chamber was destroyed. "At least it wasn't COMPLETELY useless," she thought.

 "First, it has to repair the wiring that was damaged by a..." GLaDOS made a buzzing sound. "Incident."

Chell grinned to herself and continued reading. Apparently, most commands for repair robots in this system had to be given in the form of *iterators*. There were many things mentioned, like `map()`, `filter()`, `zip()`, and also something called `generator expressions`.

 "I keep track of every cable, socket and plug in every part of the facility," the AI continued.
 
Chell raised an eyebrow. What was that in her voice, pride? "But due to the lack of visibility, I cannot confirm or deny that the amount is correct at this time."

A girl with a portal gun moved a chair to the terminal and turned it on.

-----

You need to write an `energy.py` script with a function called `fix_wiring()` which should accept three iterables (you can test the functionality with just lists) called `cables`, `sockets` and `plugs`. This function shouldn't make any assumptions about the length of these iterables, which can be different. It should return a different iterable over strings with commands like:

`plug cable1 into socket1 using plug1`
`weld cable2 to socket2 without plug`

You can see that the only iterator whose length doesn't matter is `plugs`, because in the worst case you can weld cables to sockets. If there are not enough cables or sockets, there is nothing you can do, so they shouldn't be present in a resulting iterator.

This means that for code like this:

```
plugs = ['plug1', 'plug2', 'plug3']
sockets = ['socket1', 'socket2', 'socket3', 'socket4']
cables = ['cable1', 'cable2', 'cable3', 'cable4']

for c in fix_wiring(cables, sockets, plugs):
    print(c)
```

The output should be:

```
plug cable1 into socket1 using plug1
plug cable2 into socket2 using plug2
plug cable3 into socket3 using plug3
weld cable4 to socket4 without plug
```

Also, input iterators can contain other non-string datatypes, which should be filtered out. So, for an input like:

```
plugs = ['plugZ', None, 'plugY', 'plugX']
sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
cables = ['cable2', 'cable1', False]
```

it should be just:

```
plug cable2 into socket1 using plugZ
plug cable1 into socket2 using plugY
```

Just for fun, you can get extra points if the body of your function could be written on a single line (starting with `return`), i.e. no block-starting colons (like in `if` conditions or `try/except`) are used.

## Chapter V
### Exercise 01: Personalities

 "Did you know that turrets have personalities?"

This question surprised Chell. She looked quizzically at the core.

 "Each of them is a unique combination of several random variables. They also like to sing sometimes. And you destroyed so many of them."

Chell really tried to feel sorry for the gunslingers. It wasn't easy.

 "Anyway, in order to reactivate the test chambers that were damaged during a... incident, we need to restore the production line. Vital testing equipment is needed to continue the research."

On the side of the table was a blueprint of a turret with a functional description:

```
class: Turret
personality traits: neuroticism, openness, conscientiousness, extraversion, agreeableness
actions: shoot, search, talk
```

The blueprint also had a circle of a coffee cup, a large number 427, and the name "Stanley" written in the corner.

-----

You need to implement a turret generator function called `turrets_generator()` in a file called `personality.py`. The tricky part is that you shouldn't describe the turret class separately (there is a way to dynamically generate *both* the class and the instance without using the word `class' at all).

Also, the three methods should only print `Shooting`, `Searching`, and `Talking`, respectively. Each personality trait should be a random number between 0 and 100, and the sum of all five for each instance should be 100.

## Chapter VI
### Exercise 02: Backpressure

 "You are showing great determination to repair what was broken during the... incident. Well done!"

Chell sighed and continued scrolling through the data on the terminal. The last warning she saw was about something called 'repulsion gel', whatever that meant.

 "I see you found our official experimental diet pudding substitute. This is the last task to be completed without using the handheld portal device."

Dietetic substitute? Okay, that wasn't the strangest thing she'd seen in the Aperture Science labs. Chell did some more digging and found that the automatic control valve had been reset and needed to be reconfigured.

-----

First, you need to create a file `pressure.py` with a generator function `emit_gel()` that should simulate the measured pressure of a liquid. It should generate an infinite stream of numbers from 0 to 100 (values > 100 are considered an error) with a random step sampled from the range `[0, step]`, where `step` is an argument to a generator `emit_gel()`.

Second, you must follow the pressure control guidelines. The operating pressure should be between 20 and 80, i.e. if a generator emits a value below 20 or above 80, the action that reverses the sign of the step should be applied. To implement this kind of valve, you will need to write another function called `valve()`, which will loop over the values of `emit_gel()` and use the `.send()` method to reverse the sign of the current step.

Third, you should implement an emergency break. If a pressure is above 90 or below 10, the `emit_gel()` generator should gracefully close and the script should exit.

Feel free to experiment and choose a `step` so that your script runs for a few seconds before exiting. You can add a delay between `pressure measurements` to avoid using too much CPU to generate and process the sequence.

-----

 "Thank you for participating in the repair of the laboratory equipment. Please return to the test chamber to continue your service as a test subject."

The window opened and Chell jumped from the maintenance room to the floor. GLaDOS' voice sounded much louder and more confident now.

 "I'm glad you've changed your mind and agreed that Aperture Science's goals of are more important than your so-called 'freedom'."

Chell turned her face to the camera, smiled, and covered her ears with her fingers. If her calculations were correct, the 'repulsion gel' should start filling the storage room any second now. And then it will probably get really loud for a moment.

And then she would definitely find her way out of this place. After all, she was still alive.

## Chapter VII
### Reading and tips

[Basic documentation on Python generators](https://wiki.python.org/moin/Generators).

[Wiki on lazy evaluation](https://en.wikipedia.org/wiki/Lazy_evaluation).


**Please leave your feedback [here](https://forms.gle/rnS3JCt86CJyN39B6).**
