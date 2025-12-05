# InsightLoop.AI - Backend Skeleton

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "InsightLoop.AI backend placeholder - Autonomous Web Research Agent"}
