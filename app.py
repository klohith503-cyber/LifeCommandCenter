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

    cursor.execute(
        "SELECT task FROM tasks"
    )

    tasks = cursor.fetchall()

    html = """

<!DOCTYPE html>
<html>

<head>

<title>Life Command Center</title>

<style>

body{
font-family:Arial;
background:#f5f7fb;
padding:30px;
}

.box{
max-width:700px;
margin:auto;
background:white;
padding:20px;
border-radius:20px;
}

.task{
background:#eef2ff;
padding:10px;
margin-top:10px;
border-radius:10px;
}

</style>

</head>

<body>

<div class="box">

<h1>🚀 Life Command Center</h1>

<form action="/add" method="post">

<input
name="task"
placeholder="Enter task"
required>

<button>
Add Task
</button>

</form>

<h2>Your Tasks</h2>

"""

    for task in tasks:
        html += f"""
<div class="task">
{task[0]}
</div>
"""

    html += """
</div>

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

    return HTMLResponse("""
<script>
window.location.href="/"
</script>
""")
