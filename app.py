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

```
cursor.execute(
    "SELECT task FROM tasks"
)

tasks = cursor.fetchall()

task_html=""

for task in tasks:
    task_html += f"""

    <div class='task-card'>
    {task[0]}
    </div>

    """

html=f"""
```

<!DOCTYPE html>

<html>

<head>

<title>Life Command Center</title>

<style>

body{{
background:#0f172a;
font-family:Arial;
margin:0;
color:white;
}}

.sidebar{{
position:fixed;
width:220px;
height:100vh;
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

input{{
padding:12px;
width:300px;
border-radius:10px;
border:none;
}}

button{{
padding:12px;
border:none;
border-radius:10px;
cursor:pointer;
}}

.task-card{{
background:#334155;
padding:15px;
margin-top:10px;
border-radius:10px;
}}

</style>

</head>

<body>

<div class="sidebar">

<h2>🚀 LifeOS</h2>

<p>Dashboard</p>
<p>Tasks</p>
<p>Calendar</p>
<p>Study Hub</p>
<p>Finance</p>

</div>

<div class="content">

<div class="card">

<h1>Life Command Center</h1>

<form action="/add" method="post">

<input
name="task"
placeholder="Enter task"
required>

<button>
Add
</button>

</form>

</div>

<div class="card">

<h2>Your Tasks</h2>

{task_html}

</div>

</div>

</body>

</html>

"""

```
return html
```

@app.post("/add")
async def add(task:str=Form(...)):

```
cursor.execute(
"INSERT INTO tasks(task) VALUES(?)",
(task,)
)

conn.commit()

return HTMLResponse(
```

"""

<script>
window.location.href="/"
</script>

"""
)
