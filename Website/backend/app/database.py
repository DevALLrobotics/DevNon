from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

import os
from pathlib import Path
from dotenv import load_dotenv

# 🔄 โหลด .env จากโฟลเดอร์ root (เช่น /Website/backend/.env)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# 🔧 อ่าน DATABASE_URL จาก .env
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ ตรวจสอบว่ามี DATABASE_URL จริงไหม
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in .env file")

# 🚀 สร้าง engine สำหรับ PostgreSQL แบบ async
engine = create_async_engine(DATABASE_URL, echo=True)

# 🔁 สร้าง session สำหรับใช้ในแต่ละ request
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 🧱 สร้าง Base สำหรับใช้สร้าง models
Base = declarative_base()

# 📤 dependency สำหรับใช้ใน endpoint (เช่น Depends(get_db))
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
