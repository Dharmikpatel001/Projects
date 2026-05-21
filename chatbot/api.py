from fastapi import FastAPI, HTTPException

app = FastAPI()

courses = [
    {"id": 1, "name": "Python", "fees": 5000, "duration": "2 months"},
    {"id": 2, "name": "Data Science", "fees": 12000, "duration": "4 months"},
    {"id": 3, "name": "Machine Learning", "fees": 15000, "duration": "5 months"}
]

@app.get("/")
def home():
    return{"message" : "Course API is running"}

@app.get("/courses")
def get_courses():
    return courses

@app.get("/courses/{course_name}")
def get_courses(course_name : str):
    for course in courses:
        if course["name"].lower() == course_name.lower():
            return course
    raise HTTPException(status_code=404, detail="Course Not Found")