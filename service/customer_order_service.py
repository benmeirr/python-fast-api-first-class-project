from model.customer_order import CustomerOrder
from model.customer_order_request import CustomerOrderRequest
from model.customer_order_response import CustomerOrderResponse
from repository import customer_order_repository
from service import customer_service


async def get_by_id(customer_order_id: int) -> CustomerOrder:
    return await customer_order_repository.get_by_id(customer_order_id)


async def create_customer_order(customer_order_request: CustomerOrderRequest) -> CustomerOrderResponse:
    # The selected customer from the request
    selected_customer = customer_order_request.customer

    # If the selected customer is None -> We should create new customer first
    if selected_customer.id is None:
        created_customer_id = await customer_service.create_customer(selected_customer)
        selected_customer = await customer_service.get_by_id(created_customer_id)
        customer_order_request.customer_order.customer_id = created_customer_id
    else:
        existing_customer = await customer_service.get_by_id(selected_customer.id)
        # If the provided customer has id but not existing in the DB -> We should throw an error
        if existing_customer.id is None:
            raise Exception(f"Can't find existing customer with id: {selected_customer.id}")

    customer_order_request.customer = selected_customer
    customer_order = customer_order_request.customer_order

    # Create new customer order
    await customer_order_repository.create_customer_order(customer_order)
    # Get list of all orders associated to the customer
    customer_orders = await customer_order_repository.get_by_customer_id(selected_customer.id)

    return CustomerOrderResponse(customer=selected_customer, customer_orders=customer_orders)


async def update_customer_order(customer_order_id: int, customer_order: CustomerOrderRequest) -> CustomerOrderResponse:
    pass


async def delete_by_id(customer_order_id: int):
    await customer_order_repository.delete_by_id(customer_order_id)
