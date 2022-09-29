from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

# creating the database containing 2 users.
db: List[User] = [
    User(
        id=uuid4(),
        first_name="Tammy",
        last_name="Smith",
        gender=Gender.female,
        roles=[Role.student]
         ),
    User(
        id=uuid4(),
        first_name="Alex",
        last_name="Thomas",
        middle_name="Abraham",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
         )
]

@app.get("/") # route to root
async def root():
    return {"Hello": "Orion"}

@app.get("/api/v1/users") #route to users
async def fetch_users():
    return db

# Creating endpoint for registering a new user
@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

# Creating endpoint to delete a user by their id.
@app.delete("/api/v1/users/{user_id}") #path variable is {user_id}
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {user_id} does not exists."
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return

    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user.id} does not exists."
    )




