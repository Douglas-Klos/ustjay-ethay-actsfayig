""" Flask mashup that grabs a random quote and gives us a pig latinzied version """
# pylint: disable=C0103
import os
import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """ Gets a random fact from unkno.com """
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")[0].getText().strip()
    capitals = [word[0].isupper() for word in facts.split()]
    return facts, capitals


def get_pig_latin(fact):
    """ Gets the pig latin link """
    payload = {"input_text": fact}
    response = requests.post(
        "https://hidden-journey-62459.herokuapp.com/piglatinize/", data=payload
    )
    soup = BeautifulSoup(response.content, "html.parser")
    pig_latin = soup.find("h2")
    return pig_latin.next_sibling.strip()


def format_(piglatin, capitals):
    """ Capitalize letters of piglatin """
    # We could one line this but I find it less readable.
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
    var["fact"], capitals = get_fact()
    var["piglatin"] = format_(get_pig_latin(var["fact"].replace(".", "")), capitals)
    return render_template("base.jinja2", var=var)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host="0.0.0.0", port=port)
