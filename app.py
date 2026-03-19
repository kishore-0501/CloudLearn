from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Simple in-memory databases
users_db = {}
courses_db = []


# ---------------- HOME PAGES ---------------- #

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/courses-page")
def courses_page():
    return render_template("courses.html")


# ---------------- AUTH APIs ---------------- #

@app.route("/register", methods=["POST"])
def register():

    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email in users_db:
        return jsonify({"status":"rejected","message":"User already exists"})

    users_db[email] = {
        "password":password
    }

    return jsonify({"status":"approved","message":"Registration successful"})


@app.route("/login", methods=["POST"])
def login():

    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email not in users_db:
        return jsonify({"status":"rejected","message":"User not found"})

    if users_db[email]["password"] != password:
        return jsonify({"status":"rejected","message":"Incorrect password"})

    return jsonify({"status":"approved","message":"Login successful"})


# ---------------- COURSE APIs ---------------- #

@app.route("/courses", methods=["GET"])
def get_courses():
    return jsonify(courses_db)


@app.route("/add-course", methods=["POST"])
def add_course():

    data = request.json

    course = {
        "title": data.get("title"),
        "instructor": data.get("instructor"),
        "video_url": data.get("video_url")
    }

    courses_db.append(course)

    return jsonify({"status":"approved","message":"Course added"})


# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":
    app.run(debug=True)