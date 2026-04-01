CloudLearn Application
======================

Project Overview
----------------
CloudLearn is a scalable cloud-based online learning platform developed as part of the Scalable Cloud Programming module. The application allows instructors to upload course thumbnails and short MP4 videos, while students can log in and view published courses.

The system uses:
- Flask for the web application
- Amazon S3 for storing thumbnail and video files
- AWS Lambda for processing S3 upload events
- Amazon DynamoDB for storing metadata
- Elastic Beanstalk for deployment
- Classmate Bookmarks API integration
- Custom Profile API

Project Features
----------------
1. User registration and login
2. Role-based access for student and instructor
3. Instructor course upload
4. Student dashboard for viewing courses
5. API = /login, /register, /add-course, /courses, /generate-upload-url
6. Bookmark API integration from classmate
7. Scalable cloud architecture using AWS services

Files Included
--------------
- app.py -> main Flask application
- requirements.txt -> Python dependencies
- templates/ -> HTML pages
- static/ -> CSS files
- readme.txt -> installation and execution instructions

Software Requirements
---------------------
1. Python 3.9 or above
2. pip
3. Virtual environment support
4. AWS account / AWS Academy VocLab access
5. Configured AWS permissions for:
   - S3
   - Lambda
   - DynamoDB
   - Elastic Beanstalk
   - API Gateway

Python Package Installation
---------------------------
1. Open terminal in the project folder
2. Create a virtual environment:
   python3 -m venv env

3. Activate the environment:
   source env/bin/activate

4. Install required packages:
   pip install -r requirements.txt

AWS Resources Required
----------------------
The following AWS resources must already exist or be configured:

1. S3 bucket
   - Used for storing thumbnails and videos

2. DynamoDB tables
   - users
   - courses
   - profiles

3. Lambda function
   - Triggered by S3 upload events
   - Stores uploaded file URL metadata in DynamoDB

4. API Gateway
   - Used for generate-upload-url API if configured separately

5. Elastic Beanstalk environment
   - Used to host the Flask application

Running the Application Locally
-------------------------------
1. Activate the virtual environment:
   source env/bin/activate

2. Run the Flask application:
   python app.py

3. Open in browser:
   http://localhost:8080

Cloud9 Note
-----------
If running in AWS Cloud9, make sure the Flask application uses:
- host = 0.0.0.0
- port = 8080

Example:
app.run(host="0.0.0.0", port=8080, debug=True)

Application Flow
----------------
1. Instructor logs in
2. Instructor uploads thumbnail image and video
3. Files are stored in Amazon S3
4. AWS Lambda is triggered from S3
5. Lambda stores file URLs and metadata in DynamoDB
6. Student logs in
7. Student dashboard fetches course data and displays the courses

Notes
-----
- The application uses S3 for raw media storage and DynamoDB for metadata.
- Uploaded courses are displayed on the student dashboard.
- Profile API is shared with classmates.
- Bookmarks API is consumed from a classmate service.

Author
------
Developed for academic submission as part of the Scalable Cloud Programming module.