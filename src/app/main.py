from fastapi import FastAPI

app = FastAPI(title = "API Rest To-Do",
              description = "Desenvolvimento de uma API Rest para gerenciamento de tarefas (To-Do)",
              version = "0.0.1")

@app.get("/health", tags = ["health"])
async def start_app():
    return {"detail": "API is running"}

from src.api.routes.task_routes import task_router

app.include_router(task_router)