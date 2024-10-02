# Day 05 — Python Bootcamp

## Wibbly-wobbly, timey-wimey stuff

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Fool Me Once](#exercise-00-fool-me-once)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Screwdriver Song](#exercise-01-screwdriver-song)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: Good Timing](#exercise-02-good-timing)
7. [Chapter VI](#chapter-vii) \
    7.1. [Reading](#reading)

<h2 id="chapter-i" >Chapter I</h2>
<h2 id="general-rules" >General rules</h2>

- Your scripts should not exit unexpectedly (return an error on valid input). If this happens, your project will be considered non-functional and will receive a 0 in the evaluation.
- We encourage you to create test programs for your project, even though this work doesn't have to be submitted and won't be graded. This will allow you to easily test your work and the work of your peers. You will find these tests particularly useful during your defense. In fact, you are free to use your tests and/or the tests of the peer you are evaluating during your defense.
- Submit your work to your assigned git repository. Only work in the git repository will be graded.

<h2 id="chapter-ii" >Chapter II</h2>
<h2 id="rules-of-the-day" >Rules of the day</h2>

- You should submit `*.py` and `requirements.txt` files for this task. You can also include a `README` file explaining how to start your application.
- It is also recommended to write some tests for different cases inside your scripts. To make them run only when the script is executed directly and not imported from somewhere else, you can use the `if __name__ == "__main__":` statement. You can read more about this [here](https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/).

<h2 id="chapter-iii" >Chapter III</h2>
<h2 id="intro" >Intro</h2>

 "Who was that, Doctor? We barely got out alive!"

 "They're called Daleks, one of the most merciless and violent species in the universe. Anyway, they can't get us here."

 "In this police box? By the way, why is it bigger on the inside?"

 "TARDIS dimensional modeling. Anyway, looks like we need more paper for this adventure and we're currently out of it."

 The Doctor starts running around the room, pulling some levers and pressing some buttons. It looks completely random to the untrained eye.

 "Paper? What kind, toilet?"

 "No, that probably wouldn't be a good application. It's psychic paper, see?"

 Doctor immediately shows you something with a slight resemblance to a passport. It says, "Crisis Investigator with the UN, Liverpool Division.

 "Are you really with the UN?"

 "With what now? Never mind. The thing is, it shows you what you want to see, and may save us some time. And you'll need something similar at the place we're going to."

<h2 id="chapter-iv" >Chapter IV</h2>
<h3 id="exercise-00-fool-me-once">Exercise 00: Fool Me Once</h3>

In the next moment, two strange looking devices appear from the Doctor's pockets. One looks like a very unusual screwdriver, and the other looks like a smartphone, but with a couple of tentacles on its sides.

 "So, this is an Ood species detector. If you point the tentacles at someone, it will show you the most appropriate name for that species in your language.

You take the device and point the tentacles at the Doctor. The 'smartphone' thinks for a moment and then the words 'Time Lord' appear on its screen in English.

 "Now, every species in a galactic database has a specific leader, or at least a name that will make them stumble for a moment and give you a temporary advantage."

A list of species with examples appears on one of the TARDIS screens:

```
Cyberman: John Lumic
Dalek: Davros
Judoon: Shadow Proclamation Convention 15 Enforcer
Human: Leonardo da Vinci
Ood: Klineman Halpen
Silence: Tasha Lem
Slitheen: Coca-Cola salesman
Sontaran: General Staal
Time Lord: Rassilon
Weeping Angel: The Division Representative
Zygon: Broton
```

 "Are you joking? Would you believe me if I told you, out of the blue, that I had this... Rassilon?"

 "That's not the point. The point is that most creatures would be shocked for a second at the very idea at the mere idea that you would suddenly present yourself like this. That is all we need."

You try to figure out how the device works and realize that it actually uses a WSGI+HTTP stack to present results.

Also, while plugging in some cables, Doctor gives you one last comment:

 "The Wi-Fi in the TARDIS is a bit shaky, you know, especially inside the time stream. So please please don't use any external dependencies at the moment".

---

Your goal is to implement a WSGI server with an HTTP wrapper without using any external dependencies (see the "Reading" section). It should listen on local port 8888 and parse GET parameters from a URL, for each type title giving you back a JSON (it should be HTTP code 200, also note the appropriate Content-Type header and URL encoding). An example using cURL might look like this:

```
~$ curl http://127.0.0.1:8888/?species=Time%20Lord
{"credentials": "Rassilon"}
```

If it doesn't know the type passed, it should return `{"credentials": "Unknown"}` along with HTTP status code 404.

The whole application for this task should be a single file `credentials.py`.

<h2 id="chapter-v" >Chapter V</h2>
<h3 id="exercise-01-screwdriver-song">Exercise 01: Screwdriver Song</h3>

 "So what about that device over there? Some kind of screwdriver, huh?"

 "Sonic, yeah."

 "What does it do? Can I get one?"

 "Well, it generates a combination of certain frequencies, so you can do... pretty much pretty much anything!"

 "Can it actually unscrew things?"

 "Oh, it's kind of tricky. To do that... you know what, here, just play these sound files."

---

This time we will create a simple WSGI+HTTP client-server application to manage sound files.

First, the server. It shouldn't use any kind of database, just storing files on disk is fine. The web interface should run on port 8888. When opened, the web page should show a list of already uploaded sound files and a button to upload another one. As a user, you should be able to click this button, upload the file to the server, and it should appear in a list of files displayed on the web page.

Also, the server should do a [MIME type](https://en.wikipedia.org/wiki/Media_type) check, so that only audio files are accepted (e.g. `mp3`, `ogg` and `wav`). If a non-audio file is uploaded (e.g. `jpg`, `exe` or `docx`), it should be rejected and the web page should display the message "Non-audio file detected". 

For some bonus points, you can implement playing uploaded sound files directly from the web page.

This time you are not limited to the built-in WSGI server, so it is recommended to use either the [Flask](https://flask.palletsprojects.com/) or [Django](https://www.djangoproject.com/) framework for this task, although it is not a strict requirement. Don't forget to include any third-party dependencies you use in the `requirements.txt` file. Please also include a `README` file explaining how to start the HTTP server (it should include the specific command to run).

Second, the client. This should be a command line application with two possible actions:

- `python screwdriver.py upload /path/to/file.mp3` should upload the local audio file `/path/to/file.mp3` to the server.
- `python screwdriver.py list` should retrieve and print the names of all files currently on the server.

All communication between client and server should use HTTP. It is recommended (though not required) to use either the [Requests](https://docs.python-requests.org/en/latest/) or [HTTPX](https://www.python-httpx.org/) library to perform
HTTP requests.

<h2 id="chapter-vi" >Chapter VI</h2>
<h3 id="exercise-02-good-timing">Exercise 02: Good Timing</h3>

After traveling with the Doctor for some time, you can't say you're easily surprised. But this time, the situation has somehow gotten out of control. Or at least you thought so when you saw five Time Lords hovering around the TARDIS, taking aim at the approaching Cybermen. It's not the fact that there were five of them, but rather the attempt to understand that they were all actually the same person, just from completely different time periods.

 "Allons-y!" the one in red trainers shouts enthusiastically. "No destruction, you lot,
 all right?"

 "Obviously. Everyone has their screwdrivers, right?" asks the stern one with the gray hair.

 "I think we can damage the control unit, but there's not enough power," says the one in the leather jacket. leather jacket. "But that's why we're all here, isn't it?"

 "Brilliant!" acknowledges the blonde. "So each of us... I mean me... shall take two screwdrivers instead of one and perform a sonic blast!"

The tall one in the fez turns to you and gives you a wink.

 "Just make sure I don't get in the way. You know you can do it. Trust me, I'm the Doctor!" Then he looks back at the approaching enemy and adds another word: "Geronimooo!

---

Oh, boy. We have five unpredictable Time Lords at our disposal. Think of them as threads, so there is no way to predict which one is going to act at any given moment. So you have to somehow synchronize their actions.

Each Doctor has a screwdriver in his right hand, but the minimum required to act is two. So to get two at the same time, the Doctor should grab the screwdriver of another Doctor on the left. But if everyone does this, nothing really changes, because each Doctor still has only one screwdriver left.

Start by representing both Doctors and screwdrivers as Python classes. The Doctors are numbered from 9 to 13, and each of them has to make an explosion with two screwdrivers.

*NOTE:* This is a variation of a well-known parallel programming problem, usually called the "Dining Philosophers" problem (see the link in `Reading`).

The output of your thread program should look like this:

```
Doctor 11: BLAST!
Doctor 9: BLAST!
Doctor 12: BLAST!
Doctor 10: BLAST!
Doctor 13: BLAST!
```

The order can be different on each run, because all Doctors (threads) are competing for the next turn to grab two screwdrivers. The code itself should be in the file `doctors.py`.

<h2 id="chapter-vii" >Chapter VII</h2>
<h3 id="reading">Reading</h3>

- [WSGI](https://wsgi.tutorial.codepoint.net/intro).
- [Concurrency](https://realpython.com/python-concurrency/).
- [Python Synchronization primitives](https://hackernoon.com/synchronization-primitives-in-python-564f89fee732).
- [Dining Philosophers](https://en.wikipedia.org/wiki/Dining_philosophers_problem).

**Please leave your feedback [here](https://forms.gle/5LkuABmjcwPwj6WX9).**
