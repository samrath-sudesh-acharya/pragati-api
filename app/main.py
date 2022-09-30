from fastapi import FastAPI , Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from .auth import AuthHandler
from .schemas import User


app = FastAPI()

auth_handler = AuthHandler()
users = []


@app.get('/')
def welcome():
    return  "Welcome to Pragati"

@app.post('/register',status_code=201,tags=["Authentication"])
def register(user_details: User):
    if any(x['username'] == user_details.username for x in users):
        raise HTTPException(status_code = 400,detail="Username is already taken")
    hashed_password = auth_handler.get_password_hash(user_details.password)
    users.append({
        'username': user_details.username,
        'password': hashed_password
    })
    token = auth_handler.encode_token(user_details.username)
    return {'token':token, "token_type": "bearer"}

@app.post('/login',tags=["Authentication"])
def login(user_details: User):
    user = None
    for x in users:
        if x['username'] == user_details.username:
            user = x
            break
    if (user is None) or (not auth_handler.verify_password(user_details.password,user["password"])):
        raise HTTPException(status_code  = 401,detail = 'Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'token': token,"token_type": "bearer"}

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}


