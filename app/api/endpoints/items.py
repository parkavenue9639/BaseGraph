"""
示例API端点 - 物品管理
"""
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    """物品模型"""
    id: int
    name: str
    description: str | None = None


class ItemCreate(BaseModel):
    """创建物品请求模型"""
    name: str
    description: str | None = None


# 模拟数据库
items_db: List[Item] = [
    Item(id=1, name="示例物品1", description="这是第一个示例物品"),
    Item(id=2, name="示例物品2", description="这是第二个示例物品"),
]


@router.get("/", response_model=List[Item])
async def get_items():
    """获取所有物品"""
    return items_db


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """根据ID获取物品"""
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="物品未找到")
    return item


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """创建新物品"""
    new_id = max([item.id for item in items_db], default=0) + 1
    new_item = Item(id=new_id, name=item.name, description=item.description)
    items_db.append(new_item)
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """更新物品"""
    existing_item = next((item for item in items_db if item.id == item_id), None)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="物品未找到")
    
    existing_item.name = item.name
    existing_item.description = item.description
    return existing_item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """删除物品"""
    global items_db
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="物品未找到")
    items_db = [item for item in items_db if item.id != item_id]
    return None

