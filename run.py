from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from random import *
from backend import zhihu
from furl import furl
import sys

# print(sys.path)

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


@app.route('/video/zhihu/<file_name>', methods=['GET', 'POST'])
def video_zhihu(file_name):
    if request.method == 'POST':
        content = request.get_json(silent=True)
        print(content)
        url = content.get('url', None)
        if url is None:
            return jsonify({
                "status": "error",
                "message": "下载失败，请稍后再试"
            })
        results = zhihu.download(url)
        return jsonify(results)

    file_path = furl(request.url).path
    print("download file: ", file_path)
    return redirect(file_path)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
