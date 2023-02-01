from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from util import template

todo_app = APIRouter(prefix="/todo")

@todo_app.get("/",response_class=HTMLResponse)
def index(request: Request):
    """
    Simple html response with jinja template
    html response must include a request parameter of type Request
    and that should be included in the template response context
    like below as {"request":request}
    
    """
    return template.TemplateResponse("index.html",{"request":request})