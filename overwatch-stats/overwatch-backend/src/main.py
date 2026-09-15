from fastapi import FastAPI

from routes.get_player import router as player_router

app = FastAPI()
app.include_router(player_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

