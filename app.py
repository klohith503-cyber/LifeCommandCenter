from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
app = FastAPI()
tasks = []
@app.get("/", response_class=HTMLResponse)
async def home():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Life Command Center</title>
    </head>
    <body>
        <h1>Life Command Center</h1>
        <form action="/add" method="post">
            <input name="task" placeholder="Enter task">
            <button type="submit">
            Add Task
            </button>
        </form>
        <h2>Tasks</h2>
        <ul>
        {''.join([f'<li>{task}</li>' for task in tasks])}
        </ul>
    </body>
    </html>
    """
    return html
@app.post("/add")
async def add(task: str = Form(...)):
    tasks.append(task)
    return HTMLResponse(
        content="""
        <script>
        window.location.href="/";
        </script>
        """
    )
