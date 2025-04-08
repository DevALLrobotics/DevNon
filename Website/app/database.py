from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./users.db"

# 🔧 สร้าง engine สำหรับเชื่อม SQLite แบบ async
engine = create_async_engine(DATABASE_URL, echo=True)

# 🔁 session สำหรับทำงานกับ DB
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# 📦 base สำหรับสร้าง model
Base = declarative_base()

# 📤 dependency สำหรับดึง session เข้า endpoint
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
