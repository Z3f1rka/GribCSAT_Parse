import uvicorn

from app import get_app

app = get_app()

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True)
