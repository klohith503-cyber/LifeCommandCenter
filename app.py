from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
import sqlite3
import os

app = FastAPI()

# ================= DATABASE =================

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

# ================= OPENAI =================

api_key = os.getenv("OPENAI_API_KEY")

client = None

if api_key:
    client = OpenAI(
        api_key=api_key
    )

# ================= CHAT STORAGE =================

chat_history = []

# ================= HOME =================

@app.get("/", response_class=HTMLResponse)
async def home():

    cursor.execute(
        "SELECT id,task,completed FROM tasks"
    )

    tasks = cursor.fetchall()

    completed = 0

    task_html = ""

    for task in tasks:

        checked = ""

        if task[2] == 1:
            checked = "checked"
            completed += 1

        task_html += f"""

<div style="
background:#334155;
padding:15px;
margin:10px;
border-radius:10px;
display:flex;
justify-content:space-between;
">

<div>

<input
type='checkbox'
onclick="window.location='/toggle/{task[0]}'"
{checked}
>

{task[1]}

</div>

<a href="/delete/{task[0]}">

<button>

Delete

</button>

</a>

</div>

"""

    chat_html=""

    for msg in chat_history:

        chat_html += f"""
        <p>{msg}</p>
        """

    return HTMLResponse(f"""

<html>

<head>

<title>Life Command Center</title>

<style>

body{{
background:#0f172a;
font-family:Arial;
color:white;
margin:0;
}}

.sidebar{{
position:fixed;
left:0;
width:220px;
height:100%;
background:#1e293b;
padding:20px;
}}

.content{{
margin-left:250px;
padding:30px;
}}

.card{{
background:#1e293b;
padding:20px;
border-radius:20px;
margin-bottom:20px;
}}

.ai{{
position:fixed;
right:20px;
bottom:20px;
width:330px;
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
cursor:pointer;
}}

input{{
padding:10px;
border-radius:10px;
}}

</style>

</head>

<body>

<div class="sidebar">

<h2>
🚀 LifeOS
</h2>

</div>

<div class="content">

<div class="card">

<h1>
Life Command Center
</h1>

<h3>
Tasks: {len(tasks)}
</h3>

<h3>
Completed: {completed}
</h3>

<form action="/add" method="post">

<input
name="task"
placeholder="New task"
required>

<button>

Add

</button>

</form>

</div>


<div class="card">

<h2>
Task List
</h2>

{task_html}

</div>

</div>


<div class="ai">

<h3>
🤖 AI Assistant
</h3>

{chat_html}

<form
action="/chat"
method="post"
>

<input
name="message"
placeholder="Ask anything"
required>

<button>

Send

</button>

</form>

</div>

</body>

</html>

""")


# ================= CHAT =================

@app.post("/chat")
async def chat(message: str = Form(...)):

    global chat_history

    if client:

        try:

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role":"user",
                        "content":message
                    }
                ]
            )

            answer = response.choices[0].message.content

        except Exception as e:

            answer = f"AI Error: {str(e)}"

    else:

        answer = "⚠️ OPENAI_API_KEY not configured."

    chat_history.append(
        f"<b>You:</b> {message}"
    )

    chat_history.append(
        f"<b>AI:</b> {answer}"
    )

    return HTMLResponse(
        "<script>window.location.href='/'</script>"
    )


# ================= ADD =================

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


# ================= DELETE =================

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


# ================= TOGGLE =================

@app.get("/toggle/{id}")
async def toggle(id:int):

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
