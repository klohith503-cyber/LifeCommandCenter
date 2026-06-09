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
    task TEXT,
    completed INTEGER DEFAULT 0
)
""")

conn.commit()


@app.get("/", response_class=HTMLResponse)
async def home():

    cursor.execute(
        "SELECT id, task, completed FROM tasks"
    )

    tasks = cursor.fetchall()

    task_html = ""
    completed_count = 0

    for task in tasks:

        checked = ""

        if task[2] == 1:
            checked = "checked"
            completed_count += 1

        task_html += f"""

<div class="task-card">

<input
type="checkbox"
onclick="window.location='/toggle/{task[0]}'"
{checked}
>

{task[1]}

<a href="/delete/{task[0]}">
<button>
Delete
</button>
</a>

</div>

"""

    html = f"""

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
transition:0.5s;
}}

.light{{
background:white;
color:black;
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

.task-card{{
background:#334155;
padding:15px;
margin-top:10px;
border-radius:10px;
display:flex;
justify-content:space-between;
align-items:center;
}}

button{{
padding:10px;
border:none;
border-radius:10px;
cursor:pointer;
}}

input[name="task"]{{
padding:12px;
width:300px;
border-radius:10px;
border:none;
}}

progress{{
width:100%;
height:20px;
}}

</style>

</head>

<body id="body">

<div class="sidebar">

<h2>🚀 LifeOS</h2>

<button onclick="toggleTheme()">

Dark/Light

</button>

<h3 id="clock"></h3>

</div>

<div class="content">

<div class="card">

<h2 id="greeting"></h2>

<h3>
Date:
<span id="date"></span>
</h3>

<h1>Life Command Center</h1>

<h3>
Total Tasks:
{len(tasks)}
</h3>

<h3>

Productivity:
{completed_count}/{len(tasks)}

</h3>

<progress
value="{completed_count}"
max="{max(1,len(tasks))}">
</progress>

<br><br>

<form
action="/add"
method="post"
>

<input
name="task"
placeholder="Enter task"
required
>

<button>

Add Task

</button>

</form>

</div>

<div class="card">

<h2>Your Tasks</h2>

{task_html}

</div>

</div>

<script>

function toggleTheme(){{
document.getElementById(
"body"
).classList.toggle(
"light"
)
}}

setInterval(()=>{{

document.getElementById(
"clock"
).innerHTML=
new Date().toLocaleTimeString()

}},1000)

let h=new Date().getHours()

let msg="Good Evening"

if(h<12)
msg="Good Morning"

else if(h<18)
msg="Good Afternoon"

document.getElementById(
"greeting"
).innerHTML=msg

document.getElementById(
"date"
).innerHTML=
new Date().toDateString()

</script>

</body>

</html>

"""

    return HTMLResponse(html)


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
async def delete(id: int):

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()

    return HTMLResponse(
        "<script>window.location.href='/'</script>"
    )


@app.get("/toggle/{id}")
async def toggle(id: int):

    cursor.execute(
    """

    UPDATE tasks

    SET completed=

    CASE

    WHEN completed=0
    THEN 1

    ELSE 0

    END

    WHERE id=?

    """,
    (id,)
    )

    conn.commit()

    return HTMLResponse(
        "<script>window.location.href='/'</script>"
    )
