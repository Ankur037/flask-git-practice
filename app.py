from flask import request
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["flask_todo_db"]
todos_collection = db["todos"]

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo_doc = {
        "itemName": item_name,
        "itemDescription": item_description
    }
    todos_collection.insert_one(todo_doc)

    return jsonify({"status": "success", "item": item_name}), 201
