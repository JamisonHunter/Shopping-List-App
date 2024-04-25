# Imports
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import creds

app = Flask(__name__)

# Connecting to MongoDB
client = MongoClient(creds.MONGO_URI)
db = client["shop"]
collection = db["list"]

@app.route("/")
def home():
    # Fetch all shopping lists from the database
    lists = collection.find()
    return render_template("index.html", lists=lists)

@app.route("/add_date", methods=["POST"])
def add_date():
    # Get the date from the form
    date = request.form["date"]

    # Delete the previous shopping list if it exists
    collection.delete_many({})

    # Create a new shopping list document with an empty array of items
    new_list = {"Date": date, "Items": []}

    # Insert the new list into the database
    collection.insert_one(new_list)

    # Redirect back to the home page
    return redirect(url_for("home"))

@app.route("/add_item/<list_id>", methods=["POST"])
def add_item(list_id):
    # Get the item from the form
    item = request.form["item"]

    # Update the shopping list document by appending the item to the items array
    collection.update_one({"_id": ObjectId(list_id)}, {"$push": {"Items": item}})

    # Redirect back to the home page
    return redirect(url_for("home"))

@app.route("/delete_item/<list_id>/<item_index>", methods=["GET"])
def delete_item(list_id, item_index):
    # Delete the item at the specified index from the items array
    collection.update_one({"_id": ObjectId(list_id)}, {"$unset": {f"Items.{item_index}": 1}})

    # Redirect back to the home page
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
