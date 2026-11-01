import uvicorn
from fastapi import FastAPI, status, HTTPException
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


class CategoriesSchema(BaseModel):
    id: str
    name: str


class CategoriesCreateSchema(BaseModel):
    name: str


class CategoriesUpdateSchema(BaseModel):
    name: str | None = None


tasks: list[TaskSchema] = []
categories: list[CategoriesSchema] = []


@app.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdateSchema) -> TaskSchema:
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


@app.get("/categories", status_code=status.HTTP_200_OK)
def read_categories() -> list[CategoriesSchema]:
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoriesCreateSchema) -> CategoriesSchema:
    new_category = CategoriesSchema(id=str(uuid4()), name=payload.name)
    categories.append(new_category)
    return new_category


@app.patch("/categories/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id: str, payload: CategoriesUpdateSchema) -> CategoriesSchema:
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name

            return category
    raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            break
    else:
        raise HTTPException(status_code=404, detail="Category not found")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
