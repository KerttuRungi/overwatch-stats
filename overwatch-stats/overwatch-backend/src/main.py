from fastapi import FastAPI
from routes.get_player import router as player_router
from routes.add_player import router as add_player_router
from routes.remove_player import router as remove_player_router
from routes.get_player_stats import router as player_stats_router
from routes.heros import router as heros_router
from routes.get_team_compatibility import router as team_compatibility_router
from middleware import add_cors_middleware

app = FastAPI()

app.include_router(add_player_router)
app.include_router(remove_player_router)
app.include_router(player_stats_router)
app.include_router(team_compatibility_router)
app.include_router(heros_router)
app.include_router(player_router)
add_cors_middleware(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}

