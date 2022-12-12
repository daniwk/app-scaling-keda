import asyncio
import time
from app.config import settings

from azure.servicebus import TransportType
from azure.servicebus.aio import ServiceBusClient, ServiceBusReceiver, AutoLockRenewer


CONNECTION_STR = settings.SERVICEBUS_CONNECTION_STR
QUEUE_NAME = settings.SERVICEBUS_QUEUE_NAME
WAIT_TIME = int(settings.WAIT_TIME)


async def main():
    while True:
        print('Fetching messages.')
        lock_renewal = AutoLockRenewer()
        metro_client: ServiceBusClient
        async with ServiceBusClient.from_connection_string(
                conn_str=CONNECTION_STR,
                transport_type=TransportType.AmqpOverWebsocket
        ) as metro_client:

            receiver: ServiceBusReceiver
            async with metro_client.get_queue_receiver(
                    queue_name=QUEUE_NAME,
                    auto_lock_renewer=AutoLockRenewer(max_lock_renewal_duration=120),
                    max_message_count=1
            ) as receiver:
                async for message in receiver:
                    lock_renewal.register(receiver, message, max_lock_renewal_duration=60)
                    time.sleep(WAIT_TIME)
                    await receiver.complete_message(message)
                    print("Handled message: " + str(message))

asyncio.run(main())
