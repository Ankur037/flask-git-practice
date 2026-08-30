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

<<<<<<< HEAD
@app.route("/todo")
def todo():
    return render_template("todo.html")

if __name__ == "__main__":
    app.run(debug=True)
=======
    return jsonify({"status": "success", "item": item_name}), 201
>>>>>>> f1f4f3d (Add /submittodoitem backend route storing data in MongoDB)
