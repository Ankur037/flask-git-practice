# Full Git Workflow Practice — Flask Project

Replace `Tutedude` with your actual GitHub username, and `yourname/your-repo` with your real repo path throughout.

---

## Task 1: Repository Setup & First Branch

### 1. Create a GitHub repository
On github.com → **New repository** → name it (e.g. `flask-git-practice`) → **Create repository** (don't initialize with a README if you want a totally empty repo, or do — either works, just adjust the clone step).

### 2. SSH key + clone

```bash
# Generate an SSH key (skip if you already have one at ~/.ssh/id_ed25519)
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default path, set a passphrase (or leave empty)

# Start the agent and add your key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy the public key
cat ~/.ssh/id_ed25519.pub
```

Copy that output → GitHub → **Settings → SSH and GPG keys → New SSH key** → paste → Save.

```bash
# Test the connection
ssh -T git@github.com
# Should say: "Hi Tutedude! You've successfully authenticated..."

# Clone via SSH
git clone git@github.com:yourname/your-repo.git
cd your-repo
```

### 3. Create your branch

```bash
git checkout -b Tutedude
```

### 4. Add your Flask project

```bash
mkdir -p templates static
```

**`app.py`**
```python
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

if __name__ == "__main__":
    app.run(debug=True)
```

**`data.json`**
```json
{
  "message": "Hello from the initial API version",
  "version": 1
}
```

**`templates/index.html`**
```html
<!DOCTYPE html>
<html>
<head><title>Flask Git Practice</title></head>
<body>
  <h1>Welcome</h1>
  <p>This is the base Flask app.</p>
</body>
</html>
```

**`requirements.txt`**
```
Flask==3.0.3
pymongo==4.8.0
```

### 5. Commit and merge into main

```bash
git add .
git commit -m "Add initial Flask project structure"
git push -u origin Tutedude

git checkout main
git merge Tutedude
git push origin main
```

---

## Task 2: Update JSON & Resolve Conflicts

### 6. New branch

```bash
git checkout -b Tutedude_new
```

### 7. Update the JSON used by `/api`

Edit **`data.json`**:
```json
{
  "message": "Hello from the UPDATED API version",
  "version": 2,
  "status": "active"
}
```

```bash
git add data.json
git commit -m "Update data.json for /api route"
git push -u origin Tutedude_new
```

### 8–9. Merge into main and resolve conflicts (accepting `_new`)

To actually *see* a conflict, make sure `main` also touched `data.json` differently (e.g. edit `version` to `1.5` on `main` directly and commit, before merging). Then:

```bash
git checkout main
git merge Tutedude_new
```

Git will report a conflict in `data.json` with markers like:
```
<<<<<<< HEAD
  "version": 1.5,
=======
  "version": 2,
  "status": "active",
>>>>>>> Tutedude_new
```

Resolve by **keeping the `_new` branch's version entirely**:

```bash
git checkout --theirs data.json
```

(`--theirs` = the branch being merged in, `Tutedude_new`. If you resolved by hand instead, just delete the `<<<<<<<`/`=======`/`>>>>>>>` markers and keep the `Tutedude_new` content.)

### 10. Stage, commit, push

```bash
git add data.json
git commit -m "Resolve merge conflict: accept Tutedude_new changes to data.json"
git push origin main
```

---

## Task 3: Parallel Feature Development

### 11. Create both branches from main

```bash
git checkout main
git checkout -b master_1
git checkout main
git checkout -b master_2
```

### 12. `master_1` — To-Do page (frontend)

```bash
git checkout master_1
```

**`templates/todo.html`**
```html
<!DOCTYPE html>
<html>
<head><title>To-Do</title></head>
<body>
  <h1>Add a To-Do Item</h1>
  <form action="/submittodoitem" method="POST">
    <label>Item Name:</label><br>
    <input type="text" name="itemName"><br><br>

    <label>Item Description:</label><br>
    <textarea name="itemDescription"></textarea><br><br>

    <button type="submit">Submit</button>
  </form>
</body>
</html>
```

Add a route to serve it in `app.py`:
```python
@app.route("/todo")
def todo():
    return render_template("todo.html")
```

```bash
git add templates/todo.html app.py
git commit -m "Add To-Do page with Item Name and Item Description fields"
git push -u origin master_1
```

### 13. `master_2` — Backend `/submittodoitem` route with MongoDB

```bash
git checkout master_2
```

Update **`app.py`** to add:
```python
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
```

```bash
git add app.py
git commit -m "Add /submittodoitem backend route storing data in MongoDB"
git push -u origin master_2
```

### 14. Merge both into main

```bash
git checkout main
git merge master_1
# resolve any conflicts if app.py diverged, then:
git merge master_2
# resolve conflicts (likely in app.py, since both branches touched it) — 
# keep BOTH the /todo route and the /submittodoitem route
git add app.py
git commit -m "Merge master_1 and master_2 into main"
git push origin main
```

---

## Task 4: Sequential Commits, Reset & Rebase

### 15–16. Add fields one at a time in `master_1`, one commit each

```bash
git checkout master_1
git merge main   # optional: sync master_1 with the merged main first
```

Edit `templates/todo.html`, adding **only Item ID** first:
```html
<label>Item ID:</label><br>
<input type="text" name="itemId"><br><br>
```
```bash
git add templates/todo.html
git commit -m "Add Item ID field to To-Do form"
```

Now add **only Item UUID**:
```html
<label>Item UUID:</label><br>
<input type="text" name="itemUUID"><br><br>
```
```bash
git add templates/todo.html
git commit -m "Add Item UUID field to To-Do form"
```

Now add **only Item Hash**:
```html
<label>Item Hash:</label><br>
<input type="text" name="itemHash"><br><br>
```
```bash
git add templates/todo.html
git commit -m "Add Item Hash field to To-Do form"
git push origin master_1
```

You now have three commits in sequence on `master_1`. Check them:
```bash
git log --oneline -5
```

### 17. Merge `master_1` into main

```bash
git checkout main
git merge master_1
git push origin main
```

### 18. `git reset --soft` back to the "Item ID only" state

On `main`, find the commit hash for **"Add Item ID field to To-Do form"**:
```bash
git log --oneline
```
Say it's `abc1234`. Reset to it, keeping later changes staged:
```bash
git reset --soft abc1234
```

At this point everything from the Item UUID and Item Hash commits is **staged but uncommitted**. Since the goal is to roll back to *only* the Item ID state, unstage and discard those later edits before re-committing:
```bash
git restore --staged templates/todo.html
git checkout -- templates/todo.html   # discard UUID/Hash edits, keep only Item ID content
```
*(If you want to keep the UUID/Hash edits staged instead and just recommit everything as one commit, skip the two lines above — that's a valid alternate reading of "re-commit this state.")*

Re-commit:
```bash
git add templates/todo.html
git commit -m "Re-commit: To-Do form with Item ID field only (post-reset)"
git push --force origin main   # force needed since history was rewritten
```

Merge this reset state to main (if you did the reset on a separate branch instead of directly on main, merge it now):
```bash
git checkout main
git merge <reset-branch>   # skip if you reset directly on main above
git push origin main
```

### 19. Rebase — preserve individual commits, no squash

```bash
git checkout master_1
git rebase main
```

This replays `master_1`'s commits (Item ID / Item UUID / Item Hash, and any commits since) one-by-one on top of the updated `main`, keeping each as a **separate commit** — nothing is squashed. If conflicts appear on any commit during the replay:
```bash
# fix the conflicting file(s)
git add <file>
git rebase --continue
```
Repeat until the rebase finishes. Verify history is intact:
```bash
git log --oneline --graph
```
Push the rebased branch (force needed since commit hashes changed):
```bash
git push --force origin master_1
```

---

## Quick command reference

| Action | Command |
|---|---|
| New branch | `git checkout -b <name>` |
| Switch branch | `git checkout <name>` |
| Merge | `git merge <branch>` |
| Accept "their" version in conflict | `git checkout --theirs <file>` |
| Soft reset | `git reset --soft <commit>` |
| Rebase onto main | `git rebase main` |
| Continue after conflict | `git rebase --continue` |
| Abort rebase | `git rebase --abort` |
| View history | `git log --oneline --graph --all` |
