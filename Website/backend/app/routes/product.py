from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas, database

router = APIRouter()

@router.get("/products", response_model=list[schemas.ProductOut])
async def get_all_products(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Product))
    products = result.scalars().all()
    return products

@router.get("/products/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
