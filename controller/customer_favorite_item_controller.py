from fastapi import APIRouter, HTTPException
from typing import List, Optional
from model.customer_favorite_item import CustomerFavoriteItem
from model.customer_favorite_item_request import CustomerFavoriteItemRequest
from model.customer_favorite_item_response import CustomerFavoriteItemResponse
from service import customer_favorite_item_service

router = APIRouter(
    prefix="/customer_favorite",
    tags=["customer_favorite"]
)


@router.get("/{favorite_item_id}", response_model=CustomerFavoriteItemResponse)
async def get_favorite_item(favorite_item_id: int) -> Optional[CustomerFavoriteItemResponse]:
    favorite_item = await customer_favorite_item_service.get_by_id(favorite_item_id)
    if not favorite_item:
        raise HTTPException(status_code=404, detail=f"Favorite item with id: {favorite_item_id} not found")
    return favorite_item


@router.get("/customer/{customer_id}", response_model=List[CustomerFavoriteItemResponse])
async def get_favorite_items_by_customer_id(customer_id: int) -> List[CustomerFavoriteItemResponse]:
    return await customer_favorite_item_service.get_favorite_items_by_customer_id(customer_id)


@router.post("/")
async def create_favorite_item(favorite_item: CustomerFavoriteItemRequest):
    return await customer_favorite_item_service.create_favorite_item(favorite_item)


@router.put("/{favorite_item_id}")
async def update_favorite_item(favorite_item_id: int, favorite_item: CustomerFavoriteItem):
    existing_favorite_item = await customer_favorite_item_service.get_by_id(favorite_item_id)
    if not existing_favorite_item:
        raise HTTPException(status_code=404,
                            detail=f"Can't update favorite item with id: {favorite_item_id}, item not found")
    await customer_favorite_item_service.update_favorite_item(favorite_item_id, favorite_item)
    return {"message": "Favorite item updated successfully"}


@router.delete("/{favorite_item_id}", response_model=dict)
async def delete_favorite_item(favorite_item_id: int):
    await customer_favorite_item_service.delete_by_id(favorite_item_id)
    return {"message": "Favorite item deleted successfully"}


