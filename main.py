# Imports
from flask import Flask, render_template

app = Flask(__name__)

# TODO: Connect to MongoDB client

@app.route("/")
def home():
    return render_template("index.html")

# TODO: Define CRUD routes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)