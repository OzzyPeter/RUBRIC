from fastapi import FastAPI, HTTPException, status, Path
from lecturer_dashboard import router
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
app.include_router(router)

users = {1: {"first_name":"Arinze", "email":"arinze@gmail.com", "password": "ozioma8181"}, 2: {"email":"folashade@gmail.com", "password": "ozioma1212"}}

class LoginRequest(BaseModel):
    first_name:str
    email:str
    password:str


@app.get("/")
def root():
    return {"Message": "something"}

@app.post("/login")
def login(data: LoginRequest): 
    for user_id in users:
        user = users[user_id]
        if user["email"] == data.email and user["password"] == data.password:
            return {"message": "login successful"}

        if user["email"] == data.email and user["password"] != data.password:
            return {"message": "incorrect password"}
           
    raise HTTPException(status_code=404, detail="user not found")

@app.post("/signup")
def sign_up(data: LoginRequest):
    for user_id in users:
        user = users[user_id]

        if user["email"] == data.email:
            return {"message": "Account already exists"}

    if ("@email.com" in data.email or "@gmail.com" in data.email) and len(data.password) >= 8:
        new_id = len(users) + 1

        users[new_id] = {
            "first_name":data.first_name,
            "email": data.email,
            "password": data.password
        }

        return {"message": "Account creation successful"}

    return {"message": "Invalid email or password"}










