import time
from fastapi import FastAPI,Request
from fastapi.responses import StreamingResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from users import user_app
from articles import article_app
from auth import auth_router
from todo import todo_app
from models import Base
from util import engine

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_app)
app.include_router(article_app)
app.include_router(todo_app)

# static files mount
app.mount("/media",StaticFiles(directory="media"))


@app.middleware("http")
async def just_log(request: Request, call_next):

    #before
    print("just_log midd")
    response = await call_next(request)
    return response

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    #before 
    print("add_process_time midd")
    start_time = time.time()
    response = await call_next(request)
    #after
    process_time = time.time() - start_time
    response.headers["Process-Time"] = str(process_time)
    return response




# def file_stream(filename: str):
#     """
#     for streaming responses...
#     """
#     with open(f"media/{filename}","rb") as b:
#         yield b.read()


@app.get("/download/{name}",response_class=FileResponse)
def download_file(name: str):
    return f"media/{name}"

