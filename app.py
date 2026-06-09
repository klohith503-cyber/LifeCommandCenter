
as Python code.

Delete **everything** from `app.py` first, then paste **only the code below**. Do not copy any ``` lines above or below it.

```python
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

conn = sqlite3.connect(
    "life.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
task TEXT
)
""")

conn.commit()


@app.get("/", response_class=HTMLResponse)
async def home():

    cursor.execute("SELECT id, task FROM tasks")
    tasks = cursor.fetchall()

    task_html = ""

    for task in tasks:

        task_html += f"""
<div class='task-card'>
{task[1]}
<a href="/delete/{task[0]}">
<button>Delete</button>
</a>
</div>
"""

    html = f"""

<!DOCTYPE html>
<html>

<head>

<title>LifeOS</title>

<style>

body{{
font-family:Arial;
background:#0f172a;
color:white;
margin:0;
}}

.light{{
background:white;
color:black;
}}

.sidebar{{
position:fixed;
height:100%;
width:220px;
background:#1e293b;
padding:20px;
}}

.content{{
margin-left:260px;
padding:30px;
}}

.card{{
background:#1e293b;
padding:20px;
border-radius:20px;
margin-bottom:20px;
}}

.task-card{{
background:#334155;
padding:15px;
margin-top:10px;
border-radius:10px;
}}

</style>

</head>

<body id="body">

<div class="sidebar">

<h2>🚀 LifeOS</h2>

<button onclick="toggle()">
Dark/Light
</button>

<h3 id="clock"></h3>

</div>

<div class="content">

<div class="card">

<h1>Life Command Center</h1>

<h3>Total Tasks: {len(tasks)}</h3>

<form action="/add" method="post">

<input
name="task"
required>

<button>
Add Task
</button>

</form>

</div>

<div class="card">

{task_html}

</div>

</div>

<script>

function toggle(){{
document.getElementById(
"body"
).classList.toggle(
"light"
)
}}

setInterval(()=>{{
document.getElementById(
"clock"
).innerHTML =
new Date().toLocaleTimeString()
}},1000)

</script>

</body>
</html>

"""

    return html


@app.post("/add")
async def add(task: str = Form(...)):

    cursor.execute(
    "INSERT INTO tasks(task) VALUES(?)",
    (task,)
    )

    conn.commit()

    return HTMLResponse(
"<script>window.location.href='/'</script>"
)


@app.get("/delete/{id}")
async def delete(id:int):

    cursor.execute(
    "DELETE FROM tasks WHERE id=?",
    (id,)
    )

    conn.commit()

    return HTMLResponse(
"<script>window.location.href='/'</script>"
)
