# backend/main.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# เสิร์ฟไฟล์ static (เช่น CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# หน้า index
@app.get("/")
def index():
    return FileResponse("frontend/html/index.html")

# หน้า login
@app.get("/login")
def login():
    return FileResponse("frontend/html/login.html")

# หน้า booking
@app.get("/booking")
def booking():
    return FileResponse("frontend/html/booking.html")
