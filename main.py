from flask import Flask, render_template, request, redirect
from hashlib import md5
from pymongo import MongoClient
import time

app = Flask(__name__)

mongo_client = MongoClient("localhost", 27017)
url_db = mongo_client.url.urls


@app.route('/<string:hash_url>')
def show_url(hash_url):
    pure_url = url_db.find_one({"hash_url": hash_url}, {"_id": 0, "pure_url": 1})["pure_url"]
    if pure_url.find("http://") != 0 and pure_url.find("https://") != 0:
        pure_url = "https://" + pure_url

    return redirect(pure_url, code=302)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        pure_url = request.form.get("pureURL", "")
        if pure_url == "":
            return "", 204
        pure_url_timezone = pure_url + str(time.time_ns())
        md5_url = md5(pure_url_timezone.encode()).hexdigest()[0:8]
        url_db.insert_one({"pure_url": pure_url, "hash_url": md5_url})
        return render_template("show.html", hash_url=md5_url)
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True)