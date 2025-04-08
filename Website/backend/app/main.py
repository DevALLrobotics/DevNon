from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import user, product  # 👈 เพิ่ม product

app = FastAPI()

# ✅ ให้ frontend (Next.js) เรียกได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # เปลี่ยนเป็น domain จริงใน production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ รวมเส้นทางทั้งหมด
app.include_router(user.router)     # ถ้ามี user
app.include_router(product.router)  # เพิ่ม product route

