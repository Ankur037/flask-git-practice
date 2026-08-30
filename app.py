from flask import Flask, jsonify, render_template
import json, os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api():
    path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(path) as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/todo")
def todo():
    return render_template("todo.html")

if __name__ == "__main__":
    app.run(debug=True)
