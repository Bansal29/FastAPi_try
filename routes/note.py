from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient 
from fastapi import APIRouter
from config.db import conn
from datetime import datetime
from bson import ObjectId

note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        if 'title' in doc and 'description' in doc:
            newDocs.append(
                {
                    "id": str(doc["_id"]),
                    "title": doc.get("title", ""),
                    "description": doc.get("description", "")
                }
            )
    current_date = datetime.now().strftime("%Y-%m-%d")
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs, "current_date": current_date})

@note.post("/", response_class=HTMLResponse)
async def create_item(request: Request, title: str = Form(...), description: str = Form(...)):
    form_data = {
        "title": title,
        "description": description
    }
    conn.notes.notes.insert_one(form_data)
    return RedirectResponse("/", status_code=303)

@note.post("/delete/{note_id}", response_class=HTMLResponse)
async def delete_item(note_id: str):
    conn.notes.notes.delete_one({"_id": ObjectId(note_id)})
    return RedirectResponse("/", status_code=303)
