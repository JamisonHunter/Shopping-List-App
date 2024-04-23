# Imports
from flask import Flask, render_template
from pymongo import MongoClient
import creds

app = Flask(__name__)

# Connecting to MongoDB.
client = MongoClient(creds.MONGO_URI)
db = client["astronomy"]
collection = db["apod"]

@app.route("/")
def home():
    image = collection.find_one()
    return render_template("index.html", image = image)

# TODO: Define CRUD routes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)