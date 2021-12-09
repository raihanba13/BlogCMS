from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT 
from app.auth.auth_bearer import JWTBearer
from pprint import pprint

posts = [
    {
        "id": 1,
        "title": "How to make a pancake",
        "content": '''
            1 cup all-purpose flour, (spooned and leveled)
            2 tablespoons sugar.
            2 teaspoons baking powder.
            1/2 teaspoon salt.
            1 cup milk.
            2 tablespoons unsalted butter, melted, or vegetable oil.
            1 large egg.
            1 tablespoon vegetable oil.
        '''
    }
]

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "welcome to my cooking blog!"}

@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}

@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with this ID available."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())

    pprint(posts)

    return {
        "data": "post added"
    }

users = []

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }