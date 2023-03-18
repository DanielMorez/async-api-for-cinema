from adapters.base_producer import MessageBrokerProducerClient

producer: MessageBrokerProducerClient = None


async def get_producer() -> MessageBrokerProducerClient:
    return producer
