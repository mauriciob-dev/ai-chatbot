import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from rag import load_vectorstore, get_context
from history import load_history, save_history, trim_history
from jose import jwt, JWTError

load_dotenv()

app = FastAPI()
client = Groq()
vectorstore = None

class Message(BaseModel):
    text: str
class Session(BaseModel):
    user: str

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(message: Message, request: Request):
    global vectorstore
    if vectorstore is None:
        vectorstore = load_vectorstore()

    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '')
    try:
        user_data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = user_data['key']
    user_history = load_history(username)

    context = get_context(message.text, vectorstore)

    system_prompt = "You are a helpful assistant."
    if context:
        system_prompt = f"""You are a helpful assistant. 
    Answer based on the following context from the documents:

    {context}

    If the answer is not in the context, say so honestly."""

    user_history.append({"role": "user", "content": message.text})

    response = client.chat.completions.create(
        model= "llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            *user_history
        ]
    )
    reply = response.choices[0].message.content
    user_history.append({"role": "assistant", "content": reply})

    user_history[:] = trim_history(user_history)
    save_history(user_history, username)
    return {"reply": reply}

@app.get("/login")
def login():
    return FileResponse("static/login.html")

@app.post("/session")
def session(request: Session):
    token = jwt.encode({'key': request.user}, os.getenv("SECRET_KEY"), algorithm='HS256')
    return {"token": token}


app.mount("/static", StaticFiles(directory="static"), name="static")
