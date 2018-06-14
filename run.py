from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from random import *
from backend import zhihu
from furl import furl
import sys
import os
import hashlib


basedir = os.path.abspath(os.path.dirname(__file__))

# print(sys.path)

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

cors = CORS(app, resources={"/video/*": {"origins": "*"}})

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route('/video/progress')
def video_progress():
    filename = request.args.get('filename')
    key = hashlib.md5(filename).encode('utf-8')).hexdigest()
    value = r.get(key)
    return jsonify({
        'status': 'success',
        'filename': filename,
        'out_time_ms': value,
        "message": "当前下载进度"
    })


@app.route('/video/zhihu', methods=['GET', 'POST'])
def video_zhihu():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        print(content)
        url = content.get('url', None)
        if url is None:
            return jsonify({
                "status": "error",
                "message": "下载失败，请稍后再试"
            })
        results = zhihu.download(url, directory=basedir)
        return jsonify(results)

    file = request.args.get('file')
    print("download file: ", file)
    file_path = 'video/zhihu/' + file
    return redirect(url_for('static', filename=file_path))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
