import json
import random
import sys

from flask import Flask, render_template
app = Flask(__name__)

voyages = []

def load_voyages(file_name):
    global voyages
    with open(file_name) as raw_data:
        voyages = json.load(raw_data)

def random_voyage(filter_func=None):
    global voyages
    if filter_func:
        tmp_voyages = [v for v in voyages if filter_func(v)]
    else:
        tmp_voyages = voyages
    return random.choice(tmp_voyages)

def get_voyage(key):
    global voyages
    key = key.lower()
    for v in voyages:
        if v['id'] == key or v['title'].lower() == key:
            return v

@app.route('/')
@app.route('/<voyage_key>')
def show_voyage(voyage_key=None):
    if voyage_key is None:
        voyage = random_voyage()
    else:
        voyage = get_voyage(voyage_key)
    return render_template('voyage.html', voyage=voyage)

if __name__ == '__main__':
    load_voyages(sys.argv[-1])
    app.run(port=8080, debug=True)
