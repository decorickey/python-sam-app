from fastapi import FastAPI

from routers import bmonster

app = FastAPI()
app.include_router(bmonster.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
