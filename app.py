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


def ai_reply(msg):

    msg=msg.lower()

    if "study" in msg:
        return "Study plan: 2 hrs learning + 1 hr practice + 30 min revision"

    elif "motivate" in msg:
        return "Small daily actions create huge results."

    elif "skill" in msg:
        return "Recommended: AI, Web Development, Cloud, DSA"

    elif "day" in msg:
        return "Morning: Important work | Afternoon: Deep work | Evening: Revision"

    else:
        return "I am LifeOS Assistant."


assistant_message=""


@app.get("/",response_class=HTMLResponse)
async def home():

    global assistant_message

    cursor.execute(
    "SELECT id,task,completed FROM tasks"
    )

    tasks=cursor.fetchall()

    completed=0
    task_html=""

    for task in tasks:

        checked=""

        if task[2]==1:
            checked="checked"
            completed+=1

        task_html+=f"""

<div class='task'>

<input
type='checkbox'
onclick="window.location='/toggle/{task[0]}'"
{checked}
>

{task[1]}

<a href='/delete/{task[0]}'>

<button>

Delete

</button>

</a>

</div>

"""


    return HTMLResponse(f"""

<html>

<head>

<style>

body{{
background:#0f172a;
font-family:Arial;
color:white;
margin:0;
}}

.sidebar{{
position:fixed;
width:220px;
height:100%;
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

.task{{
background:#334155;
padding:10px;
margin-top:10px;
border-radius:10px;
}}

.ai-box{{
position:fixed;
right:20px;
bottom:20px;
width:300px;
background:#1e293b;
padding:20px;
border-radius:20px;
}}

input{{
padding:10px;
}}

button{{
padding:10px;
border-radius:10px;
border:none;
}}

</style>

</head>

<body>

<div class="sidebar">

<h2>🚀 LifeOS</h2>

</div>

<div class="content">

<div class="card">

<h1>Life Command Center</h1>

<h3>
Tasks:
{len(tasks)}
</h3>

<h3>
Completed:
{completed}
</h3>

<form action="/add" method="post">

<input
name="task"
placeholder="Task"
required>

<button>
Add
</button>

</form>

</div>

<div class="card">

{task_html}

</div>

</div>

<div class="ai-box">

<h3>
🤖 Life Assistant
</h3>

<p>
{assistant_message}
</p>

<form
action="/chat"
method="post"
>

<input
name="message"
placeholder="Ask AI"
required>

<button>

Send

</button>

</form>

</div>

</body>

</html>

""")


@app.post("/chat")
async def chat(message:str=Form(...)):

    global assistant_message

    assistant_message=ai_reply(
    message
    )

    return HTMLResponse(
    "<script>window.location.href='/'</script>"
    )


@app.post("/add")
async def add(task:str=Form(...)):

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


@app.get("/toggle/{id}")
async def toggle(id:int):

    cursor.execute("""

    UPDATE tasks
    SET completed=
    CASE
    WHEN completed=0
    THEN 1
    ELSE 0
    END
    WHERE id=?

    """,(id,))

    conn.commit()

    return HTMLResponse(
    "<script>window.location.href='/'</script>"
    )
