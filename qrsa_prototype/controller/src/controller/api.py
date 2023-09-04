from fastapi import FastAPI

api = FastAPI()


@api.get("/hello")
def read_root():
    return {"Hello": "World"}


@api.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
