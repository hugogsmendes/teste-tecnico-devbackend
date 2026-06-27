from fastapi import FastAPI

app = FastAPI()

@app.get("/health", tags = ["health"])
async def start_app():
    return {"detail": "API is running"}