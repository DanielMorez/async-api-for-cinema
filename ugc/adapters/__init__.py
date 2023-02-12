from adapters.broker import MessageBrokerProducerClient, MessageBrokerConsumerClient

producer: MessageBrokerProducerClient = None
consumer: MessageBrokerConsumerClient = None


async def get_producer() -> MessageBrokerProducerClient:
    return producer


async def get_consumer() -> MessageBrokerConsumerClient:
    return consumer
