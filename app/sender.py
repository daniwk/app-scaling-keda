import json
import asyncio
from typing import List, Dict
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus.exceptions import MessageSizeExceededError

from app.config import settings

CONNECTION_STR = settings.SERVICEBUS_CONNECTION_STR
QUEUE_NAME = settings.SERVICEBUS_QUEUE_NAME
NR_MESSAGES = int(settings.NR_MESSAGES)

async def send_queue_messages(queue_name: str, messages: List[Dict]):
    """
    Sends a list of message to Service Bus Queue on which CDR to parse
    """
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
    try:
        async with servicebus_client:
            sender = servicebus_client.get_queue_sender(queue_name=queue_name)
            async with sender:
                message = [ServiceBusMessage(body=json.dumps(message)) for message in
                           messages]
                await sender.send_messages(message=message)

        print(f'Message {message} delivered to Service Bus Queue.')
    except MessageSizeExceededError:
        print(f'Message batch too big. Reduce it in half.')
        half = int(len(messages) / 2)
        await send_queue_messages(
            queue_name=queue_name, messages=messages[:half])
        await send_queue_messages(
            queue_name=queue_name, messages=messages[half:])
    finally:
        await servicebus_client.close()

async def main():
    service_bus_messages: List[Dict] = []
    for i in range(NR_MESSAGES):
        message = {"foo": "bar", "id": i}
        service_bus_messages.append(message)
    await send_queue_messages(queue_name=QUEUE_NAME, messages=service_bus_messages)

asyncio.run(main())