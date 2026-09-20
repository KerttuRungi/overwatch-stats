from fastapi import FastAPI
from routes.get_player import router as player_router
from middleware import add_cors_middleware

app = FastAPI()
app.include_router(player_router)
add_cors_middleware(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}

