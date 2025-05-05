# backend/main.py
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse , RedirectResponse, HTMLResponse
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

@app.get("/register")
def show_register():
    return FileResponse("frontend/html/register.html")

# รับข้อมูลจากฟอร์ม
@app.post("/register")
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    # 🔐 ตรงนี้คุณสามารถบันทึกลงฐานข้อมูล หรือ validate ได้
    print("📝 สมัครสมาชิกใหม่:", username, email)

    # เปลี่ยนเส้นทางกลับไปหน้าแรก (หรือแสดงข้อความสมัครสำเร็จ)
    return RedirectResponse("/", status_code=303)

# แสดงหน้า login
@app.get("/login")
def show_login():
    return FileResponse("frontend/html/login.html")

# รับข้อมูลจากฟอร์ม login
@app.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    # 🧪 (ตอนนี้ยังไม่เชื่อมฐานข้อมูล)
    # จำลอง: เช็คว่าอีเมลคือ "test@example.com" และรหัสผ่าน "1234"
    if email == "test@example.com" and password == "1234":
        print("✅ เข้าสู่ระบบสำเร็จ:", email)
        return RedirectResponse("/", status_code=303)
    else:
        print("❌ เข้าสู่ระบบล้มเหลว:", email)
        return RedirectResponse("/login", status_code=303)