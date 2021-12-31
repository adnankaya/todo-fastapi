from fastapi import FastAPI
# internals
from app.api import ping
from app.db import database, metadata, engine
from app.api import todos


app = FastAPI()
# create tables
metadata.create_all(engine)


@app.get('/ping')
def pong():
    return {'ping': 'pong'}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(ping.router)
app.include_router(todos.router, prefix='/todos', tags=['todos'])
