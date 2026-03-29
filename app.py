from flask import Flask, request, jsonify, render_template
import boto3
import uuid
import os

app = Flask(__name__)

# ---------------- DYNAMODB SETUP ---------------- #

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
users_table = dynamodb.Table("users")
courses_table = dynamodb.Table("courses")


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


@app.route("/instructor")
def instructor_page():
    return render_template("instructor.html")


# ---------------- AUTH APIs ---------------- #

@app.route("/register", methods=["POST"])
def register_user():
    try:
        data = request.get_json() or {}

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        role = data.get("role", "student")

        if not name or not email or not password or not phone:
            return jsonify({
                "status": "rejected",
                "message": "Name, email, password, and phone are required"
            }), 400

        response = users_table.get_item(Key={"email": email})

        if "Item" in response:
            return jsonify({
                "status": "rejected",
                "message": "User already exists"
            }), 200

        users_table.put_item(Item={
            "email": email,
            "password": password,
            "role": role,
            "name": name,
            "phone": phone
        })

        return jsonify({
            "status": "approved",
            "message": "Registration successful"
        }), 200

    except Exception as e:
        print("REGISTER ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "status": "rejected",
                "message": "Email and password are required"
            }), 400

        response = users_table.get_item(Key={"email": email})

        if "Item" not in response:
            return jsonify({
                "status": "rejected",
                "message": "User not found"
            }), 200

        user = response["Item"]

        if user["password"] != password:
            return jsonify({
                "status": "rejected",
                "message": "Incorrect password"
            }), 200

        return jsonify({
            "status": "approved",
            "message": "Login successful",
            "role": user.get("role", "student"),
            "name": user.get("name", ""),
            "email": user.get("email", "")
        }), 200

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
        
@app.route("/profile", methods=["GET"])
def get_profile():
    try:
        email = request.args.get("email")

        if not email:
            return jsonify({
                "status": "rejected",
                "message": "Email is required"
            }), 400

        response = users_table.get_item(Key={"email": email})

        if "Item" not in response:
            return jsonify({
                "status": "rejected",
                "message": "User not found"
            }), 404

        user = response["Item"]

        profile_letter = user["name"][0].upper() if user.get("name") else "U"

        return jsonify({
            "status": "approved",
            "profile": {
                "name": user.get("name", ""),
                "email": user.get("email", ""),
                "phone": user.get("phone", ""),
                "role": user.get("role", "student"),
                "profile_letter": profile_letter
            }
        }), 200

    except Exception as e:
        print("GET PROFILE ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
@app.route("/profile", methods=["PUT"])
def update_profile():
    try:
        data = request.get_json()

        email = data.get("email")
        name = data.get("name")
        phone = data.get("phone")

        if not email or not name or not phone:
            return jsonify({
                "status": "rejected",
                "message": "Email, name, and phone are required"
            }), 400

        users_table.update_item(
            Key={"email": email},
            UpdateExpression="SET #n = :name, phone = :phone",
            ExpressionAttributeNames={
                "#n": "name"
            },
            ExpressionAttributeValues={
                ":name": name,
                ":phone": phone
            }
        )

        return jsonify({
            "status": "approved",
            "message": "Profile updated successfully"
        }), 200

    except Exception as e:
        print("UPDATE PROFILE ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------- COURSE APIs ---------------- #

@app.route("/courses", methods=["GET"])
def get_courses():
    try:
        response = courses_table.scan()
        items = response.get("Items", [])

        return jsonify(items), 200

    except Exception as e:
        print("GET COURSES ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/add-course", methods=["POST"])
def add_course():
    try:
        data = request.get_json()

        title = data.get("title")
        instructor = data.get("instructor")
        category = data.get("category")
        thumbnail = data.get("thumbnail")
        video_url = data.get("video_url")
        description = data.get("description")

        if not title or not instructor or not video_url or not description:
            return jsonify({
                "status": "rejected",
                "message": "Title, instructor, video URL, and description are required"
            }), 400

        course_id = str(uuid.uuid4())

        courses_table.put_item(Item={
            "course_id": course_id,
            "title": title,
            "instructor": instructor,
            "category": category if category else "Cloud Computing",
            "thumbnail": thumbnail if thumbnail else "",
            "video_url": video_url,
            "description": description
        })

        return jsonify({
            "status": "approved",
            "message": "Course published successfully"
        }), 200

    except Exception as e:
        print("ADD COURSE ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------- OPTIONAL DEBUG API ---------------- #

@app.route("/get-users", methods=["GET"])
def get_users():
    try:
        response = users_table.scan()
        return jsonify(response.get("Items", [])), 200

    except Exception as e:
        print("GET USERS ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------- RUN SERVER ---------------- #

#if __name__ == "__main__":
 #   port = int(os.environ.get("PORT", 8080))
  #  app.run(host="0.0.0.0", port=port, debug=True)