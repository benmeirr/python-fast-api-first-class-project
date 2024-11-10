from typing import Optional

from api.internalApi.seller_service.model.item_response import ItemResponse
from repository.database import config
import httpx


async def get_lowest_price_item_by_name(item_name: str) -> Optional[ItemResponse]:
    url = f"{config.SELLER_SERVICE_BASE_URL}/item/search/"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"item_name": item_name})
            response.raise_for_status()

            data = response.json()

            item = ItemResponse(
                id=data.get('id'),
                item_name=data.get('item_name'),
                price=data.get('price')
            )
            return item

        except httpx.HTTPStatusError as exc:
            print(f"No items found with name: {item_name}")
            return None


async def get_item_by_item_id(item_id: int) -> Optional[ItemResponse]:
    url = f"{config.SELLER_SERVICE_BASE_URL}/item/{item_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            data = response.json()

            item = ItemResponse(
                id=data.get('id'),
                item_name=data.get('item_name'),
                price=data.get('price')
            )
            return item

        except httpx.HTTPStatusError as exc:
            print(f"No item found with item id: {item_id}")
            return None



