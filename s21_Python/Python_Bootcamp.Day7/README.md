# Day 07 — Python Bootcamp

## Is there a difference?

💡 [Tap here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) **to leave your feedback on the project**. It's anonymous and will help our team make your educational experience better. We recommend completing the survey immediately after the project.

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Retirement Plan](#exercise-00-retirement-plan)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Human Life](#exercise-01-human-life)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: For the Future](#exercise-02-for-the-future)
7. [Chapter VI](#chapter-vii) \
    7.1. [Reading](#reading)

<h2 id="chapter-i" >Chapter I</h2>
<h2 id="general-rules" >General rules</h2>

- Your scripts should not exit unexpectedly (return an error on valid input). If this happens, your project will be considered non-functional and will receive a 0 in the evaluation.
- Submit your work to your assigned git repository. Only the work in the git repository will be evaluated.

<h2 id="chapter-ii" >Chapter II</h2>
<h2 id="rules-of-the-day" >Rules of the day</h2>

- You should submit `*.py` and `requirements.txt` files for this task, as well as a "database" file with questions, and "tests" and "docs" folders with appropriate content.
- The documentation from EX02 should be buildable using the `make html` command.

<h2 id="chapter-iii" >Chapter III</h2>
<h2 id="intro" >Intro</h2>

 "It seems you feel our work is of no benefit to the public."
 
 "Replicants are like any other machine. They're either a benefit or a danger. If they're a benefit, it's not my problem."
 
 "May I ask you a personal question?"

Deckard sat down in a chair.
 
 "Sure."
 
 "Have you ever retired a human by mistake?"
 
 "No," he didn't even blink.
 
 "But in your position, that's a risk?"

Deckard prepared to give a meaningful answer, but then another person appeared in the room.
It was a tall man, probably in his fifties, wearing an immaculate black suit and some sort of kind of high-tech, multifaceted glasses.

<h2 id="chapter-iv" >Chapter IV</h2>
<h3 id="exercise-00-retirement-plan">Exercise 00: Retirement Plan</h3>

 "Is this an empathy test? Capillary dilation of the so-called blush response? Fluctuation of the pupil? Involuntary dilation of the iris?"

 "We call it Voight-Kampff for short."

Rachael decided to stick with the formalities.

 "Mr. Deckard, Dr. Eldon Tyrell," she introduced.

 "Demonstrate it. I want to see it work," Tyrell seemed impatient. A characteristic of people with very busy schedules.

Several minutes passed and the discussion continued. Even though he was young and bold, Deckard realized that the Voight-Kampff test was much more dangerous than it seemed. A lot of work had to be had to be done to make it reliable.

-----

You need to create your own version of the [Voight-Kampff Test](https://bladerunner.fandom.com/wiki/Voight-Kampff_test).
To do this, you should prepare a set of questions (at least 10 is sufficient) with three or four randomly selected answers. These questions and answers should be stored in a separate file of any format (e.g. SQLite or just JSON).

After each answer, a set of variables should be manually entered by a person
asking the questions:

- Respiration (measured in BPM, usually about 12-16 breaths per minute),
- Heart rate (usually around 60 to 100 beats per minute),
- Blushing level (categorical, 6 possible levels),
- Pupillary dilation (current pupil size, 2 to 8 mm).

After ten questions and variable measurements, the test should print a strict binary decision as to whether a responding subject is a human or a replicant. In this exercise, you can invent your own logic to make this decision.

Try to split your business logic into separate files based on the tasks the components solve. The starting script should be called `main.py`. All interaction with the test should be via the command line.

<h2 id="chapter-v" >Chapter V</h2>
<h3 id="exercise-01-human-life">Exercise 01: Human Life</h3>

For a few days after his interaction with Rachael and Tyrell, Deckard couldn't stop thinking about the reliability of the test. He had always blindly followed its results, but could he trust the test itself?

All the research led him to the fact that the human body has surprisingly few responses to an external stimulus that could be called "fully automatic". Of course, Rick couldn't reproduce all the research behind Voight-Kampff, but he wanted to know the algorithm.

Deckard couldn't really explain why, even to himself. One of the most dangerous thoughts was, "I need to know the right answers if I am ever going to be a test subject.

-----

You already have the implementation of the test from EX00. But does it really work? In this exercise, you must write tests to cover all possible positive and negative cases.

What if the question file is empty? Could it be that, based on the data, there is an equal probability of an output being human or replicant?

Your VK test implementation probably consists of several functions and, presumably, classes. Your goal here is to cover all corner cases for all components with tests. Basically, whenever a test operator enters something wrong (such as selecting a non-existent answer or out-of-bounds numbers for measurements, e.g., negative heart rate), he or she should receive a meaningful information message and a chance to repeat the input.

During this exercise, you will most likely rewrite at least some of the code from EX00, but that's the point. It is also highly recommended that you use the Pytest framework when writing tests (see the section below). All tests should be in the `tests` directory.

<h2 id="chapter-vi" >Chapter VI</h2>
<h3 id="exercise-02-for-the-future">Exercise 02: For the Future</h3>

...But did it matter? After everything that happened in the next week, the line between human and Replicant had practically disappeared for Deckard. He knew it existed because the test said it did, but that was all he had.

The Blade Runners still had to use the test to hunt down the escaped Replicants. It was their way of making sure they were doing the right thing.

 "What are you working on?" Rachael asked him one day. 

 "I want to... write about it. I think it's more of a work of art for me now than a weapon."

 "You never answered me... Have you ever taken the test yourself?"

 "Don't worry about it. Cogito, ergo sum."

-----

You need to use Sphinx Project to automatically generate documentation for your code written in EX00/EX01.

The resulting documentation should consist of at least two parts:

- Quickstart, which is the description of how to work with the test;
- Auto-generated reference about the code (see link to Sphinx Autodoc in the Reading section).

For the first part, you can use either Markdown or RST for the text and formatting.
For the second part, you'll need to add comments to all entities in your code - modules, functions, classes, etc. You can find a link to the guide on how to write docstrings in the Reading section.

You should also add a proper title and logo to your project for the documentation. Don't include the generated docs in your submission though, it should be buildable with `make html` on your peer's side if all the requirements are installed.

<h2 id="chapter-vii" >Chapter VII</h2>
<h3 id="reading">Reading</h3>

- [Python Testing Guideline](https://realpython.com/pytest-python-testing).
- [Python Sphinx Tutorial](https://www.sphinx-doc.org/en/master/tutorial/index.html).
- [Writing Docstrings](https://realpython.com/documenting-python-code/).
- [Sphinx Autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).

