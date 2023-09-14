from fastapi import FastAPI, status
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


#class
class student(BaseModel):
  name: str
  branch: str
  mobile: str

#database connection

try:
  conn = psycopg2.connect(host='localhost', database='py_fastapi', user='postgres', password='0000', cursor_factory= RealDictCursor)
  cursor = conn.cursor()
  print("Database connected successfully!!!")

except Exception as error:
  print("Database connection failed...")
  print("Error: ", error)



@app.post("/students",status_code=status.HTTP_201_CREATED)
def cretate_post(stu: student):

  cursor.execute(""" INSERT INTO students(name, branch, mobile) values(%s, %s, %s) returning * """,(stu.name, stu.branch, stu.mobile))

  new_student=cursor.fetchone()

  conn.commit()

  return {"new_student": new_student}


@app.get("/students")
def get_students():
  cursor.execute(""" SELECT * FROM students""")
  students = cursor.fetchall()
  return {"students": students}
