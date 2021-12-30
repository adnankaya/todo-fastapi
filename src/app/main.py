from fastapi import FastAPI
from app.api import ping

app = FastAPI()



@app.get('/ping')
def pong():
    return {'ping':'pong'}


app.include_router(ping.router)