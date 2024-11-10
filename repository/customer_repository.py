import json
from typing import Optional

from model.customer import Customer
from model.customer_status import CustomerStatus
from repository import cache_repository
from .database import database

TABLE_NAME = "customer"


async def get_by_id(customer_id: int) -> Optional[Customer]:
    if cache_repository.is_key_exists(str(customer_id)):
        string_customer = cache_repository.get_cache_entity(str(customer_id))
        customer_data = json.loads(string_customer)
        return Customer(**customer_data)
    else:
        query = f"SELECT * FROM {TABLE_NAME} WHERE id=:customer_id"
        result = await database.fetch_one(query, values={"customer_id": customer_id})
        if result:
            customer = Customer(**result)
            cache_repository.create_cache_entity(str(customer_id), customer.json())
            return customer
        else:
            return None


async def get_all() -> list[Customer]:
    query = f"SELECT * FROM {TABLE_NAME}"
    results = await database.fetch_all(query)
    return [Customer(**result) for result in results]


async def create_customer(customer: Customer) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (first_name, last_name, email, status)
        VALUES (:first_name, :last_name, :email, :status)
    """
    values = {"first_name": customer.first_name, "last_name": customer.last_name,
              "email": customer.email, "status": customer.status.name}

    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")

    customer.id = last_record_id[0]
    cache_repository.create_cache_entity(str(customer.id), customer.json())

    return customer.id


async def update_customer(customer_id: int, customer: Customer):
    if cache_repository.is_key_exists(str(customer_id)):
        cache_repository.update_cache_entity(str(customer_id), customer.json())

    query = f"""
        UPDATE {TABLE_NAME}
        SET first_name = :first_name,
        last_name = :last_name,
        email = :email
        status = :status
        WHERE id = :customer_id
    """
    values = {"customer_id": customer_id, "first_name": customer.first_name,
              "last_name": customer.last_name, "email": customer.email, "status": customer.status.name}
    await database.execute(query, values)


async def delete_by_id(customer_id: int):
    cache_repository.remove_cache_entity(str(customer_id))

    query = f"DELETE FROM {TABLE_NAME} WHERE id=:customer_id"
    await database.execute(query, values={"customer_id": customer_id})


async def get_by_status(customer_status: CustomerStatus):
    query = f"SELECT * FROM {TABLE_NAME} WHERE status=:customer_status"
    results = await database.fetch_all(query, values={"customer_status": customer_status.name})
    return [Customer(**result) for result in results]

