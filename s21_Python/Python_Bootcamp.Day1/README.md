# Day 01 — Python Bootcamp

## Trolling is a art

Help three honorable gentlemen to figure out the better way!

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Functional Purse](#exercise-00-functional-purse)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Splitwise](#exercise-01-splitwise)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: Burglar Alarm](#exercise-02-burglar-alarm)  
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
- Your script (or scripts) for this day should have all functions on the top level of the file, so that they can possibly be imported for checking.
- It is encouraged (and graded as a bonus) to write some tests for various cases inside your scripts as well. To make them run only when the script is executed directly and not imported from somewhere else, you can use the `if __name__ == "__main__":` statement. You can read more about this [here](https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/).

## Chapter III
### Intro

 "Gentlemen," Tom began. "I think we can agree that every single thing is determined by a set of properties it possesses. Like this stone, for example." He tapped a huge granite boulder where he was sitting. "It has a certain weight, height and proportions, doesn't it?"

 "With all due respect, I disagree," Bert argued. "It's not about its parameters, it's about what it can do, or what you can do with it!"

 "Okay, my friends," William interjected. "Here's my purse." He fished it out of his pocket and placed it on a large stump near the campfire. A purse made a squeaking sound. "Its main purpose is to hold gold bars. It currently holds three. The two things are inseparable when talking about it. Am I wrong?"

 "You are and you are not, honorable William," Bert replied. "The fact that it holds three bars of gold is only its condition."

He took a long branch and began to draw letters in the ashes of the campfire, like this:
```
purse = {"gold_ingots": 3}

```

 "So, to add a new bar to a purse, you have to perform a certain action, right?" Bert started to write something like that:

```
def add_ingot(purse):

```

 "Just a moment, kind sir," Tom interrupted. "Why do I have to write a function when I can just do it like this?"

He picked up another branch and drew:

```
purse["gold_ingots"] += 1

```

 "Sure, you can, but that means you're making assumptions about a purse that you can't know for sure! For example, what if it is empty? How..."

```
purse = {}

```

Tom immediately realized that his approach would not work in this case. 

 "This is what I tend to call [Domain-driven design] (https://en.wikipedia.org/wiki/Domain-driven_design)," Bert said. "We write specifically what we want to do and just use standard primitives to help us do it."


## Chapter IV
### Exercise 00: Functional Purse

 "So, Bert, I see you are a distinguished gentleman!" exclaimed William. "So how would you design my purse?"

You need to write the functions `add_ingot(purse)`, `get_ingot(purse)`, and `empty(purse)` that take a purse (a dictionary, which is strictly speaking a `typing.Dict[str, int]`) and return a purse (an empty dict in the case of `empty(purse)`). You should not make any assumptions about the contents of of the purse (it can be empty or hold something completely different, like "stones").

Also, your functions shouldn't have side effects. This means that an object passed as an argument should not be modified inside a function. Instead, it should return a new object. So you *shouldn't* use the code Tom wrote, because it makes a *direct assignment* to a field inside a wallet. You should instead return a *new dict instance* with an updated number inside.

So a function composition like `add_ingot(get_ingot(add_ingot(empty(purse))))` should return
`{"gold_ingots": 1}`. Also, getting an ingot from an empty purse shouldn't cause an error and should just return an empty one.

Note: We are only interested in gold bars in this task, so it doesn't really matter what happens to the rest of the stuff in the purse. You can keep it or throw it away.

## Chapter V
### Exercise 01: Splitwise

 "Just a moment, kind sirs," said Tom. "How is all this going to help us divide the booty? If we have several bags after the hunt, how will we decide who gets what?"
 
 "Don't worry, my friend!" William patted Tom gently on the shoulder. "A guiding star will help us!"
 
 "A star? How?"

 "How do you implement a function so that it can take one, two, or many objects as arguments?"

 "Oh, I get it now, thanks!" And then Tom and William started working on an honest algorithm.

They need to write a function called `split_booty` that takes any number of purses (dictionaries) as arguments. Purses in arguments can contain various items, but our honorable men are only interested in gold ingots (named `gold_ingots` as in the examples above). The number of ingots can be zero or a positive integer.

This function should return three purses (dictionaries) such that in any two of the three purses the difference between the number of ingots is not greater than 1. For example, if the booty contains `{"gold_ingots":3}`, `{"gold_ingots":2}`, and `{"apples":10}`, then the function should return `({"gold_ingots": 2}, {"gold_ingots": 2}, {"gold_ingots": 1})`.

While implementing this function, you still shouldn't use direct assignment to fields within dictionaries. Instead, you can reuse functions you wrote in EX00. 

## Chapter VI
### Exercise 02: Burglar Alarm

Bilbo Baggins, or "The Burglar" as he now liked to call himself, hid in the bushes and listened quietly to three giant trolls discussing rather interesting things. He didn't really understand most of it, but at least it was about booty, wallets, and bars. So he pretty much convinced himself that this discussion was somehow related to his "specialty" when he decided to steal William's purse. And just as his hand was about to grab it from a stump (the trolls were still in the middle of a rather heated discussion), it suddenly made a very loud squeaking noise.

And he immediately realized that there were now three pairs of troll eyes staring directly at him.

 "Sir William," Bert began after a short pause, looking at the Hobbit who froze in fear, "I see you've managed to set up some protective measures. That's brilliant! Is it an additional feature in your functional design?"

 "Well," William replied, "I think you've already noticed that this particular bag is rather "squeaky," so to speak. That's because when someone tries to do something funny with it, it makes a noise and I know about it right away. It's because of its special, hmm, "decoration"..."

 So far you have written several functions (`add_ingot(purse)`, `get_ingot(purse)` and `empty(purse)`) for the purse design, but now you need to find a way to add some new behavior to all of them — whenever one of them is called, `SQUEAK` should be printed. The trick is that you can't change the body of these functions, but still provide this alarm. The hint William mentioned about "special decorations" may help you with this.

-----

Even after the purse design was perfected and the burglar was caught red-handed, the trolls couldn't stop arguing about whether "action" was more or less important than "feature".

But by then it was too late. Or, on the other hand, too early — morning came, and the first rays of sunlight appeared over the horizon. The trolls turned to stone almost immediately, and Bilbo was finally able to breathe a sigh of relief when he saw Gandalf approaching from the forest.

 "I knew it was your idea!" said the Hobbit enthusiastically. "You imitated their voices so they wouldn't stop fighting, didn't you?"

 "Not really, my honorable Burglar," the old wizard objected. "This is what happens when various trolls spend too much time comparing object-oriented programming styles to functional programming. But it's a very dark magic you shouldn't really worry about, my friend..."
 
## Chapter VII
### Reading and tips

The "don't assign directly" rule may seem confusing, so here's what's behind it: in functional programming, all objects, including data structures, are generally immutable.
This means that it is considered bad practice to change the data inside a container; instead, a new container with a new value should be created.
For example, if you have a list `a = [1, 2, 3]` and you want to increase the second element by five, instead of writing `a[1] += 5` you should create another object: `b = [a[0], a[1] + 5, a[2]]`.
This approach may seem odd, but sometimes when you're dealing with a large codebase, it helps a lot to know that your data won't be accidentally changed somewhere deep in your code, because nothing is mutable.

Also, Python has some immutable object types out of the box, e.g. [frozensets](https://docs.python.org/3/library/stdtypes.html#frozenset).

As an additional cool feature, Python has a built-in way to change the behavior of functions without directly modifying their code.
It is called a `decorator` and is just a special syntax for a function that takes a function as an argument and returns a function. You can read [this article](https://realpython.com/primer-on-python-decorators/) for more details and examples.  

**Please leave your feedback [here](https://docs.google.com/forms/d/e/1FAIpQLSc9IEAPVeHKnBGZKmG6cZOaQwPX-W0vwa3-mjjm4LsBs0jr3g/viewform?usp=sf_link)**
