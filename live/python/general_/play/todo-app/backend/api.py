from fastapi import FastAPI
from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    desc: str

todos: list[Todo] = []

app = FastAPI()

@app.get('/')
async def home():
    return 'Hello World'

@app.get('/todos')
async def get_todos():
    return todos

@app.post('/todos')
async def add_todo(todo: Todo):
    todos.append(todo)
    return todo

@app.post('/add-todo')
async def addd_todo(title: str, desc: str):
    todo = Todo(title=title, desc=desc)
    todos.append(todo)
    return todo

@app.get('/hello')
async def say_hi(name: str):
    return f'Hello {name.title()}?'