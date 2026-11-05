from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

class MemberCreate(BaseModel):
    name: str
    email: str
    age: int



@app.get("/members", response_model=list[MemberResponse])
#response_model=list[MemberResponse] => 여러명 반환
def get_members():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, email
                FROM members
                ORDER BY id
                """
            )

            members = cur.fetchall()
    return members

@app.post("/members", 
 response_model=MemberResponse,
 status_code=201)

def insert_members(member:MemberCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO public.members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, age
                """,
                (member.name, member.email, member.age)
                

            )

            members = cur.fetchall()
    return members    
