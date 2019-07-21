import os

import requests
from flask import Flask, send_file, Response, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """ Gets a random fact from unkno.com """
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    capitals = [False] * len(facts[0].getText().strip().split())
    for count, word in enumerate(facts[0].getText().strip().split()):
        if word[0].isupper():
            capitals[count] = True

    return facts[0].getText().strip(), capitals


def get_pig_latin(fact):
    """ Gets the pig latin link """
    payload = {'input_text': fact}
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/", data=payload)
    soup = BeautifulSoup(response.content, "html.parser")
    pig_latin = soup.find("h2")
    return pig_latin.next_sibling.strip() + '.'


def format_(piglatin, capitals):
    """ Capitalize letters of piglatin """
    split = piglatin.split(' ')
    output = []
    for count, word in enumerate(split):
        if capitals[count] is True:
            output.append(word.capitalize())
        else:
            output.append(word)

    return " ".join(output)


@app.route('/')
def home():
    var = {}
    var['fact'], capitals = get_fact()
    var['piglatin'] = get_pig_latin(var['fact'].replace('.', ''))
    var['piglatin'] = format_(var['piglatin'], capitals)

    return render_template("base.jinja2", var=var)

    # """" Contruct and return body """
    # body = "<h1>Original quote</h1>"
    # fact = get_fact()
    # body += '<p style="text-indent :5em;" >' + fact + "</pre><br><br><hr>"
    # pig_latin = get_pig_latin(fact)
    # body += "<h1>Pig Latin</h1>"
    # body += '<p style="text-indent :5em;" >' + pig_latin  + "</pre>"
    # return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
