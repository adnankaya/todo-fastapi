from typing import List
from fastapi import APIRouter, HTTPException, Path
from app.api import crud
from app.api.models import TodoSchema, TodoDB


router = APIRouter()


@router.post('/', response_model=TodoDB, status_code=201)
async def create_todo(payload: TodoSchema):
    todo_id = await crud.post(payload)

    response = {
        'id': todo_id,
        'title': payload.title,
        'description': payload.description
    }
    return response


@router.get('/{id}/', response_model=TodoDB)
async def read_todo(id: int = Path(..., gt=0)):
    todo = await crud.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    return todo


@router.get('/', response_model=List[TodoDB])
async def read_todos():
    todos = await crud.get_all()
    return todos


@router.put('/{id}/', response_model=TodoDB)
async def update_todo(payload: TodoSchema, id: int = Path(..., gt=0)):
    todo = await crud.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_id = await crud.put(id, payload)
    response = {
        'id': todo_id,
        'title': payload.title,
        'description': payload.description
    }
    return response


@router.delete('/{id}/', response_model=TodoDB)
async def delete_todo(id: int = Path(..., gt=0)):
    todo = await crud.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')

    await crud.delete(id)
    return todo
