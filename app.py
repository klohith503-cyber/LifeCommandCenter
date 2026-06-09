
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

templates = Jinja2Templates(directory="templates")

tasks=[]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks
        }
    )

@app.post("/add")
async def add(task:str = Form(...)):

    tasks.append(task)

    return {"message":"Task added"}
