from fastapi import FastAPI

from routes.get_player import router as player_router
from routes.add_player import router as add_player_router
from routes.get_player_stats import router as get_player_stats_summary

app = FastAPI()
app.include_router(player_router)
app.include_router(add_player_router)
app.include_router(get_player_stats_summary)



@app.get("/")
async def root():
    return {"message": "Hello World"}

