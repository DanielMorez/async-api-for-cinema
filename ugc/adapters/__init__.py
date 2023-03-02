from adapters.broker import (MessageBrokerConsumerClient,
                             MessageBrokerProducerClient)

producer: MessageBrokerProducerClient = None
consumer: MessageBrokerConsumerClient = None


async def get_producer() -> MessageBrokerProducerClient:
    return producer


async def get_consumer() -> MessageBrokerConsumerClient:
    return consumer
