""" Flask mashup that grabs a random quote and gives us a pig latinzied version """
# pylint: disable=C0103
import os
import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


# We could one line most of these functions, but it makes them less readable.


def get_fact():
    """ Gets a random fact from unkno.com """
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all("div", id="content")[0].getText().strip()


def get_capitals(fact):
    """
    Determines if each word in the fact starts with a capital letter
    Returns a list of bools representing each word, True if it is upper
    """
    return [word[0].isupper() for word in fact.split()]


def get_link(fact):
    """ Gets the pig latin link """
    return requests.post(
        "https://hidden-journey-62459.herokuapp.com/piglatinize/",
        data={"input_text": fact.strip(".")},
        allow_redirects=None,
    ).headers["Location"]


def get_pig_latin(link):
    """ Gets the pig latin from link """
    soup = BeautifulSoup(requests.get(link).content, "html.parser")
    pig_latin = soup.find("h2")
    return pig_latin.next_sibling.strip()


def format_(piglatin, capitals):
    """ Capitalize words in piglatin and add trailing period """
    split = piglatin.split(" ")
    output = [
        word.capitalize() if capitals[count] is True else word
        for count, word in enumerate(split)
    ]
    return " ".join(output) + "."


@app.route("/")
def home():
    """ Our main page """
    var = {}
    var["fact"] = get_fact()
    capitals = get_capitals(var["fact"])
    var["link"] = get_link(var["fact"])
    var["piglatin"] = format_(get_pig_latin(var["link"]), capitals)
    return render_template("base.jinja2", var=var)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host="0.0.0.0", port=port)
