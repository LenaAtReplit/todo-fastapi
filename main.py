from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI()


class TodoItem(BaseModel):
  # Define the schema for a Todo item
  name: str
  completed: bool


# In-memory storage for TODO items
todos: List[TodoItem] = []

@app.get("/")
def read_root():
  return FileResponse('index.html')


@app.get("/todos", response_model=List[TodoItem])
def read_todos():
  # Endpoint to get a list of all TODO items
  return todos


@app.post("/todos", response_model=TodoItem)
def create_todo(todo_item: TodoItem):
  # Endpoint to create a new TODO item
  todos.append(todo_item)
  # Print the updated todos list to console
  print("Updated Todos List:")
  for todo in todos:
    print(todo)
  return todo_item


@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo_item: TodoItem):
  # Endpoint to update an existing TODO item by ID
  if todo_id >= len(todos) or todo_id < 0:
    raise HTTPException(status_code=404, detail="Todo not found")

  todos[todo_id] = todo_item
  return todo_item


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
  # Endpoint to delete a TODO item by ID
  if todo_id >= len(todos) or todo_id < 0:
    raise HTTPException(status_code=404, detail="Todo not found")

  del todos[todo_id]
  return {"detail": "Todo deleted successfully"}
