import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


tasks: list[TaskSchema] = []


@app.get("/tasks", status_code=200)
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code=201)
def create_tasks(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
