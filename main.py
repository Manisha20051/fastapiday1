from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Todo API",
    description="A simple in-memory Todo API built with FastAPI",
    version="1.0.0",
)

# Pydantic schema for creating a Todo item
class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# Pydantic schema for updating a Todo item (optional fields)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# Temporary in-memory dictionary to store items
# Key: todo ID (int) -> Value: todo details (dict)
todos: dict[int, dict] = {}
next_id: int = 1


@app.get("/")
def root():
    return {
        "message": "Welcome to the FastAPI Todo List API!",
        "docs": "/docs",
        "todos_url": "/todos",
    }


@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos():
    """Retrieve all todo items."""
    return list(todos.values())


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo(todo_id: int):
    """Retrieve a single todo item by ID."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with ID {todo_id} not found",
        )
    return todos[todo_id]


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(item: TodoItem):
    """Create a new todo item and store it in the temp dictionary."""
    global next_id
    todo_data = {
        "id": next_id,
        "title": item.title,
        "description": item.description,
        "completed": item.completed,
    }
    todos[next_id] = todo_data
    next_id += 1
    return todo_data


@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo(todo_id: int, item: TodoUpdate):
    """Update an existing todo item by ID."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with ID {todo_id} not found",
        )

    stored_item = todos[todo_id]

    # Update only fields provided in the request
    if item.title is not None:
        stored_item["title"] = item.title
    if item.description is not None:
        stored_item["description"] = item.description
    if item.completed is not None:
        stored_item["completed"] = item.completed

    return stored_item


@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_id: int):
    """Delete a todo item by ID."""
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with ID {todo_id} not found",
        )
    deleted_item = todos.pop(todo_id)
    return {
        "message": f"Todo item with ID {todo_id} deleted successfully",
        "deleted_item": deleted_item,
    }