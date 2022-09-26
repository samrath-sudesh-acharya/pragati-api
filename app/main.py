import imp

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def welcome():
    return  "Welcome to Pragati"