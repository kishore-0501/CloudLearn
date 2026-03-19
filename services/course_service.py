# services/course_service.py
courses_db = []

def add_course(title, instructor, video_url):
    course_id = len(courses_db) + 1
    course = {
        "id": course_id,
        "title": title,
        "instructor": instructor,
        "video_url": video_url
    }
    courses_db.append(course)
    return {"status": "approved", "course_id": course_id}

def get_courses():
    return courses_db