from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import random, csv
from csv import writer

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)


@app.route("/")
def index():
    return "<div style='height:100%; width:100%; display:flex; align-items:center; justify-content:center;'>Welcome to DeJokes API.</div>"

@app.route("/joke")
@limiter.limit("100/minute")
def getJoke():
    with open(r"C:\Users\Seb\Desktop\.dust\dejokes\jokes.txt") as f:
        reader = csv.reader(f, delimiter='`')
        jokes = list(reader)

        return jokes[random.randint(0, len(jokes)-1)]

@app.route("/submit/<joke>/<answer>/<twitter>")
@limiter.limit("2/minute")
def submitJoke(joke, answer, twitter):
    if len(joke) > 10:
        if len(answer) > 4:
            if len(twitter) > 3:
                with open(r"C:\Users\Seb\Desktop\.dust\dejokes\jokes.txt", 'a', newline='') as f:
                    poet = csv.writer(f, delimiter='`')
                    poet.writerow([joke, answer, twitter])
                return "{'code': 202, 'response': 'Thank you for your joke!'}"
            else:
                return "{'code': 400, 'response': 'Please include valid twitter username.}"
        else:
            return "{'code': 400, 'response': 'Please include an answer more than 4 characters.}"
    else:
        return "{'code': 400, 'response': 'Please include a joke more than 10 characters.}"


if __name__ == "__main__":
    app.run(host='0.0.0.0')


# <link rel='shortcut icon' href='https://i.imgur.com/5TG1bsF.png' type='image/x-icon'>