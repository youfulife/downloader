from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from random import *
import sys

print(sys.path)

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

cors = CORS(app, resources={"/api/*": {"origins": "*"}})


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/zhihu')
def zhihu():
    url = request
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
