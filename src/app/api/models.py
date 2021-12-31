from pydantic import BaseModel


class TodoSchema(BaseModel):
    title: str
    description: str


class TodoDB(TodoSchema):
    id: int
