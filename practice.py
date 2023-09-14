from fastapi import FastAPI, Response, status, HTTPException
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


#getting student details by id
@app.get("/students/{id}")
def get_student(id: str):
  cursor.execute(""" SELECT * FROM students WHERE id = %s """,(id))
  student = cursor.fetchone()

  print(student)
  if not student:
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
  
  return {"student": student} 


#deleting student
@app.delete("/students/{id}")
def delete_student(id: str):
  cursor.execute(""" DELETE from students WHERE id = %s returning *""", (id))
  deleted_student = cursor.fetchone()

  conn.commit()

  if deleted_student == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")

  #return {"daleted student": deleted_student}
  return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/students/{id}")
def update_student(id: str, stu: student):
  cursor.execute(""" update students set name=%s, branch=%s, mobile=%s where id=%s returning * """, (stu.name, stu.branch, stu.mobile, id))
  updated_student = cursor.fetchone()

  print(updated_student)
  conn.commit()

  if updated_student == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

  return {"updated student":updated_student}
  