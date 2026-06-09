from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
import sqlite3
import os

app = FastAPI()

# ---------------- AI ----------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

chat_history=[]

# ---------------- Database ----------------

conn = sqlite3.connect(
    "life.db",
    check_same_thread=False
)

cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
task TEXT,
completed INTEGER DEFAULT 0
)
""")

conn.commit()


# ---------------- Home ----------------

@app.get("/",response_class=HTMLResponse)
async def home():

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

<div class='task-card'>

<div>

<input
type='checkbox'
onclick="window.location='/toggle/{task[0]}'"
{checked}
>

{task[1]}

</div>

<a href='/delete/{task[0]}'>

<button>

Delete

</button>

</a>

</div>

"""

    chat_html=""

    for msg in chat_history:

        chat_html+=f"<p>{msg}</p>"


    return HTMLResponse(f"""

<html>

<head>

<style>

body{{
margin:0;
background:#0f172a;
font-family:Arial;
color:white;
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

.task-card{{
display:flex;
justify-content:space-between;
padding:15px;
background:#334155;
margin-top:10px;
border-radius:10px;
}}

.ai-box{{
position:fixed;
right:20px;
bottom:20px;
width:350px;
height:450px;
overflow:auto;
background:#1e293b;
padding:20px;
border-radius:20px;
}}

button{{
padding:10px;
border:none;
border-radius:10px;
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

<h3>Total Tasks:
{len(tasks)}
</h3>

<h3>Completed:
{completed}
</h3>

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


<div class="ai-box">

<h3>🤖 AI Assistant</h3>

{chat_html}

<form
action="/chat"
method="post"
>

<input
name="message"
placeholder="Ask anything..."
required>

<button>

Send

</button>

</form>

</div>

</body>

</html>

""")


# ---------------- Chat ----------------

@app.post("/chat")
async def chat(message:str=Form(...)):

    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
            "role":"user",
            "content":message
            }
        ]
    )

    answer=response.choices[0].message.content

    chat_history.append(
    f"<b>You:</b> {message}"
    )

    chat_history.append(
    f"<b>AI:</b> {answer}"
    )

    return HTMLResponse(
    "<script>window.location.href='/'</script>"
    )


# ---------------- Add Task ----------------

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


# ---------------- Delete ----------------

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


# ---------------- Toggle ----------------

@app.get("/toggle/{id}")
async def toggle(id:int):

    cursor.execute("""
    UPDATE tasks
    SET completed=
    CASE
    WHEN completed=0 THEN 1
    ELSE 0
    END
    WHERE id=?
    """,(id,))

    conn.commit()

    return HTMLResponse(
    "<script>window.location.href='/'</script>"
    )
