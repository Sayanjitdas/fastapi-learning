from fastapi import FastAPI
from fastapi.responses import StreamingResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from users import user_app
from articles import article_app
from auth import auth_router
from models import Base
from util import engine

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_app)
app.include_router(article_app)

# static files mount
app.mount("/media",StaticFiles(directory="media"))

# def file_stream(filename: str):
#     """
#     for streaming responses...
#     """
#     with open(f"media/{filename}","rb") as b:
#         yield b.read()

@app.get("/download/{name}",response_class=FileResponse)
def download_file(name: str):
    return f"media/{name}"
