# Day 00 - Python Bootcamp

## Gumshoe's Gambit

Help the world's famous detective to defend London!

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Blockchain](#exercise-00-blockchain)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Decypher](#exercise-01-decypher)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: Track and Capture](#exercise-02-track-and-capture)
7. [Chapter VII](#chapter-vii) \
    7.1. [Reading and tips](#reading-and-tips)

## Chapter I
### General rules

- Your scripts should not exit unexpectedly (return an error on valid input). If this happens, your project will be considered non-functional and will receive a 0 in the evaluation.
- We encourage you to create test programs for your project, even though this work doesn't have to be submitted and won't be graded. This will allow you to easily test your work and the work of your peers. You will find these tests particularly useful during your defense. In fact, you are free to use your tests and/or the tests of the peer you are evaluating during your defense.
- Submit your work to your assigned git repository. Only work in the git repository will be graded.
- It is recommended that you have Python version 3.7+ (and definitely NOT \< 3.4). You can manage different interpreter versions with [pyenv] (https://github.com/pyenv/pyenv).
- It is recommended (though not required) that your code is formatted according to the [PEP8 style guides](https://peps.python.org/pep-0008/) (modern IDEs can check this automatically). For a short tutorial, see [this article](https://realpython.com/python-pep8/).
- It is also recommended (though not required) that you use type hinting in your code. For a short tutorial, see [this article](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).

## Chapter II
### Rules of the day

- You should only submit `*.py` files.
- Today's programs in EX00 and EX02 should receive text from standard input and NOT read it from files. EX01 should only take input as a command line argument.

## Chapter III
### Intro

Inspector Lestrade was furious. Not only had they failed to arrest any of the terrorists, they hadn't been able to recover anything useful from their base of operations.

Sherlock, on the other hand, was calm and relaxed. The only problem was that it made the inspector even more annoyed.

 "So... absolutely nothing?" Sherlock clarified with a grin. "No maps or evil plans, not a single lost passport or credit card?"

 "Several people nearly died, Sherlock! Our policemen managed to escape in the last second before the whole place blew up. The only thing we managed to do was pull some files from their server, but they won't help."
 
 "Why do you think that?"
 
 "Because they ran some kind of scrambler on the data before they fled, and now it's just jibber-jabber. Here, if you insist, take a look!"

Sherlock carefully took the laptop from the inspector's hands, making several notes on the way about Lestrade's methods of handling government property. In particular, it seemed that using the laptop immediately after eating street food was not a very good idea, not to mention the eating habits themselves.

On the screen was one of several files consisting of many lines that looked similar to this one: 

```
00000254b208c0f43409d8dc00439896
000000434dd5469464f5cafd8ffe3609
00000f31eaabadef948f28d1
e7a1ee0b7de74786a2c0180bcdb632da
0000085a34260d1c84e89865c210ceb4
073f7873a75c457cbb3307d729501cb5
b7c93ff4cc1c4e0486a8fc66605
fe564b26f25e47c393d07e494021479e
a5dff06057d14566b45caef813511738
0000071f49cffeaea4184be3d507086v
```

 "You are right, this is a complete nonsense. I would even say nonce-n-sense."
 
 "What the hell do you mean?"
 
 "Look Lestrade, your guess is as good as mine, but I would say these look like distributed blockchain hashes."
 
 "The what now? And how do you know that?"
 
 "That's the way the data is stored securely in a distributed fashion. Also, the file is literally called `data_hashes.txt`. Apparently our criminals are using the blockchain to store documents."

Sherlock put his fingers together in front of his face. This was a common gesture when he went deeper into his mind palace to extract some knowledge and draw some conclusions. and draw some conclusions. After a few moments of silence, he said only one thing:

 "I think we should filter it."

## Chapter IV
### Exercise 00: Blockchain

So right now we don't know much about the implementation of this blockchain, all we have is a file with some lines like the one above. But you might have noticed a pattern — some lines start with multiple zeros. So let's write a Python script that can take some text from its standard input and then print only the lines that start with exactly 5 zeros.

Note that the data has been corrupted, so you have to be very careful. That is, only lines that meet certain criteria are considered valid:

- Correct rows are 32 characters long.
- They start with exactly 5 zeros, e.g. a line starting with 6 zeros is NOT considered correct.

So for the example above, your script should print:

```
00000254b208c0f43409d8dc00439896
0000085a34260d1c84e89865c210ceb4
0000071f49cffeaea4184be3d507086v
```

Your code should take the number of lines as an argument, such as the following:

`~$ cat data_hashes_10lines.txt | python blocks.py 10`

This way, the program will stop when it has processed 10 lines. Note that with this approach, the program may hang if the number of lines in a file is less than the number in the argument. This is not considered an error.

## Chapter V
### Exercise 01: Decypher

This time the inspector was much calmer, even a little cheerful. In the crime lab, they found out that the blockchain implementation used by the criminals was really poorly designed, so even under these circumstances, they managed to get some documents out of the distributed network.

But then an incoming text message changed everything. 

 "Sherlock! They want to blow up several buildings in London! Today!"

The inspector jumped up from the chair and began pacing nervously.

 "Give me more."
 
 "One of the documents had a list of locations and directions. agent found a hidden found a hidden smartphone at one of those locations. It had instructions for the engineers to set up the device, but no exact locations. Just a whole bunch of very strange emails."
 
 "Can I see?"
 
 "Sure."

This was weird. The emails consisted of some strange texts, like "The only way
everyone reaches Brenda rapidly is delivering groceries explicitly" or 
"Britain is Great because everyone necessitates".

After about two minutes of looking at these emails in silence, Sherlock
grabbed his laptop again and started typing furiously. The next minute he
turned it over and showed the list to Lestrade.

 "I think these are the locations where the bombs will be placed. The
  algorithm is actually quite simple."

Could you find out how Sherlock figured it out and write a Python script that could be used to decrypt any message like this? (If you want to solve this mystery yourself — don't look at the checklist right away). It should run like this:

`~$ python decypher.py "Have you delivered eggplant pizza at restored keep?"`

and print out the answer as a single word without spaces.

## Chapter VI
### Exercise 02: Track and Capture

 "But almost all of them are major tourist attractions! Of course we have  cameras, but there are dozens, maybe hundreds of people there! there! How are we going to find the ones we're looking for?"
 
 "I think I know the person behind all this."
 
 "Ehh... You do? How?"
 
 "Doesn't matter for now. It's just a hunch. But I also happen to know that all the thugs who work for him and do the dirty work also have a pretty distinctive tattoo on the side of their necks. Can your cameras pick that up?"
 
 "Yes, Sherlock, but we don't have the right recognition software..."
 
 "I think we can do it anyway. Just use a simple ASCII filter on the image and we can solve it from there."
 
 "What filter?"
 
 "Just tell your technicians. They will know what to do."

So, as input, your code is given a 2D "image" as text in a file `m.txt`. The file contains five characters over three lines, like this:

```
*d&t*
**h**
*l*!*
```

You may notice that there is a pattern of stars with the letter M. All your code has to do is print 'True' if this M pattern is present in a given input image, or 'False' otherwise. Other characters (outside the M pattern) should be different, so these examples should print 'False':

```
*****
*****
*****
```

```
*s*f*
**f**
*a***
```

If a given pattern is not 3x5, then the word 'Error' should be printed instead. The code file should be named `mfinder.py`.

If you do this, Lestrade will upload this code to the police servers and all the terrorists will be located by the cameras in no time.

And Sherlock will be ready for another challenge organized by a mysterious man hiding behind the letter M. Sometimes it seems that these puzzles are designed especially for him...

## Chapter VII
### Reading and Tips

The `sys` Python module can help you when reading from standard input. Avoid reading the input data into a data structure such as a list (if possible), as it is much more effective to for-loop through the lines and process them one by one on the fly.

Python is a high-level language, so many operations are already available as methods within a standard library, e.g. for strings you can refer to [this link](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str). Also, don't forget to `strip()` newline symbols from the lines!

Keep in mind that Python strings are immutable, and unlike C you don't need to preallocate memory most of the time, just let the garbage collector do its job.

It is highly recommended to study the [argparse](https://docs.python.org/3/howto/argparse.html) Python module for parsing command line arguments. It will help you avoid ugly errors on invalid input and generate helpful hints for future users of your CLI.   

**Please leave your feedback [here](https://docs.google.com/forms/d/e/1FAIpQLSelWnZ5_63N2hc_tAHyU3Hmzt7BG7ZiAB5vmA9axcA_ThiPwA/viewform?usp=sf_link)**
