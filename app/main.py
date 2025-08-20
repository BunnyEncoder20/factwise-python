from fastapi import FastAPI
from app.routers import users, teams, boards

app = FastAPI(title="Project Board API")

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(boards.router)
