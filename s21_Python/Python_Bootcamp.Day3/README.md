# Day 03 - Python Bootcamp

## Computer repair with a smile

Fight the system, help the people!

## Contents

1. [Chapter I](#chapter-i) \
    1.1. [General rules](#general-rules)
2. [Chapter II](#chapter-ii) \
    2.1. [Rules of the day](#rules-of-the-day)
3. [Chapter III](#chapter-iii) \
    3.1. [Intro](#intro)
4. [Chapter IV](#chapter-iv) \
    4.1. [Exercise 00: Innocent Prank](#exercise-00-innocent-prank)
5. [Chapter V](#chapter-v) \
    5.1. [Exercise 01: Cash Flow](#exercise-01-cash-flow)
6. [Chapter VI](#chapter-vi) \
    6.1. [Exercise 02: Deploy](#exercise-02-deploy)
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

It was a quiet evening outside, but the work inside the abandoned arcade was far from done. Mobley and Trenton were in the middle of a heated debate about various attack vectors, while Darlene was looking at a bulletin board with photos of high-ranking members of Evil Corp's management. Elliot sat in the corner, muttering to himself as usual. 

"Okay everyone, listen up!" Darlene was as loud as ever, so even arguing hackers immediately shut up. "Let's start with the little things. We need to show the people that Evil Corp is not to be trusted with their money."

## Chapter IV
### Exercise 00: Innocent Prank

 "Mobley, do you have a sample money transfer form?"

 "I sure do. Take a look at the file 'evilcorp.html' in a shared folder."

 "Perfect. Remember, you can just run `python3 -m http.server` in a directory with that file to test out our little our little trick in a browser. Just go to http://127.0.0.1:8000/evilcorp.html and you'll see the form for yourself. And then Elliot... brother, are you even listening?"

Elliot turned his chair to show that he was interested.

 "Now, you only get one shot at this. Your script has to call an actual HTML file on an Evil Corp. server. The more people who see the message that they have been hacked, the better."

Trenton immediately showed a script on her screen that needed to be inserted into a web page:

```
 <script>
        hacked = function() {
            alert('hacked');
        }
        window.addEventListener('load', 
          function() { 
            var f = document.querySelector("form");
            f.setAttribute("onsubmit", "hacked()");
          },
          false
        );
</script>
```

 "Let's call this operation... [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)!"

-----

You need to write a Python script "exploit.py" that will do several things:

- First, it needs to read a file called "evilcorp.html".
- Second, it should change the page title (in `<title>` tags) to "Evil Corp - Stealing your money every day".
- Third, it should parse the user's name from the page (including the pronoun) and insert a new `<h1>' tag  into the `body' of a page, saying `<h1>Mr. Robot, you are hacked!</h1>`, where "Mr. Robot" is a parsed pronoun and name.
- Fourth, it must also insert a Trenton's script into the `body` of a page. If all goes well, you should see the word "hacked" appear in an alert window when you press the `Send' button.
- Finally, the link at the bottom of a page should now point to "https://mrrobot.fandom.com/wiki/Fsociety" with the actual name of the company on the page replaced with "Fsociety".

The new HTML file should be named "evilcorp_hacked.html" and placed in the same directory as the source "evilcorp.html" file.

## Chapter V
### Exercise 01: Cash Flow

After a while, Elliot turned his laptop over on the table and showed the script. Mobley gave him a thumbs up and Trenton switched places with Darlene near the bulletin board.

 "Well, this is a nice little distraction, but the real attack is going to happen somewhere else. We know that Evil Corp is using [Redis](https://redis.io/) pubsub as a queue broker. But we can only deploy a script once, so..."

 "...so we need a test environment, I get it." Mobley flicked a piece of popcorn and quickly caught it. "I'm on it."

-----

You need to write two scripts - `producer.py` and `consumer.py`.

Producer needs to generate JSON messages like this:

```
{
   "metadata": {
       "from": 1023461745,
       "to": 5738456434
   },
   "amount": 10000
}
```

and put it as payload into a Redis pubsub queue. All account numbers ('from' and 'to') should be exactly 10 digits. Additional points can be earned if the code uses the built-in `logging` module (instead of the `print` function) to write generated messages to stdout for manual testing.

Consumer should be given an argument with a list of account numbers like this:

`~$ python consumer.py -e 7134456234,3476371234`

where `-e` is a parameter receiving a list of bad guy account numbers. When started, it should read messages from a pubsub queue and print them to stdout, one line at a time. For accounts in the bad guys list, if they are specified as a recipient, the consumer should *swap* sender and recipient for the transaction. But this should *only* happen if "amount" is not negative.

For example, if producer generates three messages like this

```
{"metadata": {"from": 1111111111,"to": 2222222222},"amount": 10000}
{"metadata": {"from": 3333333333,"to": 4444444444},"amount": -3000}
{"metadata": {"from": 2222222222,"to": 5555555555},"amount": 5000}
```

consumer started like `~$ python consumer.py -e 2222222222,4444444444` should print out:

```
{"metadata": {"from": 2222222222,"to": 1111111111},"amount": 10000}
{"metadata": {"from": 3333333333,"to": 4444444444},"amount": -3000}
{"metadata": {"from": 2222222222,"to": 5555555555},"amount": 5000}
```

Note that only the first line was changed. The second wasn't changed because "amount" was negative (even though the receiver is a bad guy). The third wasn't changed because the bad guy is a sender, not a receiver.

## Chapter VI
### Exercise 02: Deploy

 "Perfecto!" Darlene was thrilled. "Now all we have to do is write a deployment script."
 
 "I can do that!" Trenton had pretty good [Ansible](https://docs.ansible.com/ansible/latest/index.html) skills. "Once Elliot is in, all he has to do is install a bunch of packages on a server, copy over our exploit and consumer, and run them!"

As she spoke, Elliot's fingers ran around a keyboard, creating a todo list and saving it to todo.yml. Everything was ready.

-----

You don't need to know Ansible intimately to complete this exercise. It would be nice if you could test your code through it, though it's not required. There is a list of tasks that should be placed in a generated deploy.yml file in YAML format:

- Install packages;
- Copy files;
- Execute files on a remote server using a Python interpreter with appropriate arguments.

These tasks should be generated in Ansible notation (e.g. look [here](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html) for notation
on copying files). The script should be named 'gen_ansible.py'.

Thus, your code should convert Elliot's 'todo.yml' into 'deploy.yml' following this notation.

## Chapter VII
### Reading and tips

Working with HTML is one of the typical tasks when writing parsers and various server code in Python. Two of the most widely used libraries for this are [lxml](https://lxml.de/) and the aforementioned [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). They are not mutually exclusive though, as lxml can be used as a parsing backend for BS4, combining great performance with pretty good API flexibility. You can read about parsing backends [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser).

Working with Redis is also a pretty common task to encounter in the world of applied Python. And it can also be optimized by using an optional [low-level C wrapper](https://github.com/redis/hiredis-py). It is not a necessary requirement in this task, but still a good module to know about.

Working with YAML is also a very common task for which [PyYAML](https://pyyaml.org/) is often used. Parsing config files or writing Ansible plugins is something you may come across if Python is used as your team's language for dealing with infrastructure. It would take a lot of time and text to introduce a specific YAML format for this task, so we'll use an existing standard. Even though it takes some time and effort to study, it can be really helpful to know the basics of Ansible for your future job or just daily automation tasks.

By the way, just in case you're curious, Ansible [supports Windows](https://docs.ansible.com/ansible/latest/user_guide/windows_usage.html) as well!    

**Please leave your feedback [here](https://forms.gle/dfKBUNyBKs9mvcWYA)**
