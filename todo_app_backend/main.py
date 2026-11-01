import uvicorn
from fastapi import FastAPI, status
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


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[TaskSchema] = []


@app.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
        return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
