# Day 09 - Python Bootcamp

## Fast and Curious

💡 [Tap here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) **to leave your feedback on the project**. It's anonymous and will help our team make your educational experience better. We recommend completing the survey immediately after the project.

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Still Counts](#exercise-00-still-counts)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Split-Second](#exercise-01-split-second)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: Autopilot](#exercise-02-autopilot)

## Chapter I
### General rules

- Your scripts should not exit unexpectedly (return an error on valid input). If this happens, your project will be considered non-functional and will receive a 0 in the evaluation.
- Submit your work to your assigned git repository. Only the work in the git repository will be evaluated.

## Chapter II
### Rules of the day

- You should turn in `*.py`, `*.c`, `*.pyx` and `requirements.txt` (if using external dependencies) files for this task.

## Chapter III
### Intro

 "Oh come on, Dom, you've been racing for years, you're telling me you've never configured an [ECU](https://en.wikipedia.org/wiki/Engine_control_unit)?"
 
 It was obvious that Letty wasn't angry, just playful.
 
 "Aren't those always proprietary and sealed?"
 
 "Not really, if you have the right equipment," she poked him in the forehead with a dirty mechanic's glove. "Especially here."
 
 "Okay, then. So it should respond to a bunch of sensors and do it really fast."
 
 Toretto pulled a laptop from the table and set it on a toolbox in front of him. He wanted to to connect to the device, but Letty raised her hand.
 
 "I know how you usually like to dig too deep. Let's start with something simple."

## Chapter IV
### Exercise 00: Still Counts

Letty pulled up a chair and sat down astride it.

 "You know the main problem with Python? It's flexible, but slow. That's not a problem unless you want to have a fast thing that's flexible to control."
 
Dominic scratched his head for a second, then nodded.

 "We have to fall back to C in those cases, right?"

 "For example. I know you already know basic C. Anyway, I doubt it will be a problem
 for you to write a function to, say, add two numbers?"
 
-----

You need to write a simple calculator module for Python (using the Python C API) with four functions:

- `add(a, b)`
- `sub(a, b)`
- `mul(a, b)`
- `div(a, b)`

This module should consist of two files - 'calculator.c' and 'setup.py' to build it.
In the regular part of EX00 let's assume that the numbers are integers:

```python
>>> import calculator
>>> calculator.add(14.5, 21.87)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: integer argument expected, got float
>>> calculator.add(14, 21)
35
>>> calculator.sub(14, 21)
-7
>>> calculator.mul(14, 21)
294
>>> calculator.div(14, 7)
2
```

Also, your code should handle zero-division errors properly by throwing a built-in Python exception from the C code:

```python
>>> import calculator
>>> calculator.div(14, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: Cannot divide by zero
```

The module should contain only the two files mentioned above and be installable with `python setup.py install`.

BONUS: Update your calculator code to handle both int and float values for both operands.

## Chapter V
### Exercise 01: Split-Second

The engine roared a few times outside and in a few minutes a garage door opened.

 "Brian, come on!" Toretto waved invitingly. "Have you ever programmed an ECU?"
 
Letty giggled, but tried to hide it. 
 
 "Hey Dominic! Well, not really, but I know what the main challenge is."
 
 "Making it go as fast as possible? Like with cars in general?"
 
"Actually, it's to make it go *SURELY* faster than it did before. You know how computers measure time?"
 
Dominic raised an eyebrow, but Letty answered immediately: 
 
 "Every computer has at least two kinds of clocks — one that stores the current time and one that measures periods of it, so a machine can compare them."
 
 "Exactly!" Brian smiled. "So when it comes to fractions of a second, there is a physical crystal on a board that vibrates at a certain frequency. To compare two time deltas, all you have to do is look at two numbers that are guaranteed to strictly increase tick by tick as time passes.
 
 "Oh, now I remember," Dominic stood up to shake Brian's hand. "That's why digital have monotonic clocks."
 
-----

You need to use a built-in `ctypes` library in Python to implement an interface to a monotonic clock in your operating system. Windows, Linux, and MacOS have this as part of a standard library. Python [also has it now](https://peps.python.org/pep-0418/#time-monotonic), but you should write your own version from scratch.

It should be a function `monotonic()` in a file called `monotonic.py` and a returned value should be in seconds (some OSes also support nanoseconds). 

## Chapter VI
### Exercise 02: Autopilot

Preparations for the heist were nearly complete, with roles assigned and equipment upgraded. One of the advanced prototypes included a machine learning power steering control unit. Its main purpose was to save the driver's life at all costs during possible collisions and dangerous situations by analyzing the surroundings with cameras and depth sensors.

Dominic pulled Brian aside for a few minutes before the briefing.

 "You know, some of the people on this team are like family to me. Including you. We've talked a lot this morning about computers and controllers — can you tell me again that this device will do its best to keep everyone safe? Is it fast enough?"
 
 "You know, this is a top-notch prototype created by some very smart people."
 
 "I know. I just needed confirmation. Do you have any idea how it actually works?"
 
Brian smiled and then just whispered a sentence, trying to sound as creepy as possible:

 "It multiplies matrices!"
 
-----

This time you need to use a third way to speed up computation in Python, which is [Cython](https://cython.org/).
We won't go into Data Science, but [multiplying matrices](https://en.wikipedia.org/wiki/Matrix_multiplication) is a fairly simple and straightforward procedure.

The example simplified Python code for it might look something like this:

```python
from itertools import tee 

def mul(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]
```

You have to write your own function `mul()` in Cython (filename is `multiply.pyx`) and (as in EX00) implement a proper `setup.py` file to make a Python package called 'matrix':

```python
from matrix import mul

x = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
y = [[1,2],[1,2],[3,4]]

print(mul(x, y))
"""[[12, 18], [27, 42], [42, 66], [57, 90]]"""
```

For simplicity, let's say that your code should only work with integers and matrices no larger than 100x100. Also, don't use the built-in implementation from [Numpy](https://numpy.org/) for this task, even though in production code that would probably be one of the preferred ways.

BONUS: Write a performance test in `test_mul_perf.py` comparing the basic pure Python implementation with your Cython one. It should be much faster.

