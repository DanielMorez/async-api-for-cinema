import functools
import logging
import time
from typing import List

import pika

from config import settings
logger = logging.getLogger(__name__)


class RabbitMQConsumerClient:
    def __init__(self):
        self.url = f"amqp://{settings.RABBITMQ__USER}:{settings.RABBITMQ__PASSWORD}@{settings.RABBITMQ__HOST}:{settings.RABBITMQ__PORT}"
        self.params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=settings.RABBITMQ__QUEUE)
        self.channel.basic_consume(
            queue=settings.RABBITMQ__QUEUE,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        print("Start read from queue")


class BaseConsumer:
    def __init__(self, parameters, on_message, current_logger=logger):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.
        """
        self.should_reconnect = False
        self.was_consuming = False

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tags = []
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1
        self.parameters = parameters
        self.on_message = on_message
        self.logger = current_logger

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.
        :rtype: pika.SelectConnection
        """
        # consumer = RabbitMQConsumerClient()
        # consumer.channel.start_consuming()
        self.logger.info("Connecting...")
        credentials = pika.PlainCredentials(
            self.parameters.get("USERNAME"), self.parameters.get("PASSWORD")
        )
        parameters = pika.ConnectionParameters(
            self.parameters.get("HOST"), credentials=credentials
        )
        return pika.SelectConnection(
            parameters=parameters,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

    def close_connection(self):
        self._consuming = False
        if self._connection:
            if self._connection.is_closing or self._connection.is_closed:
                self.logger.info("Connection is closing or already closed")
            else:
                self.logger.info("Closing connection")
                self._connection.close()

    def on_connection_open(self, _unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.
        :param pika.SelectConnection _unused_connection: The connection
        """
        self.logger.info("Connection opened")
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.
        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error
        """
        self.logger.error("Connection open failed: %s", err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.
        :param pika.connection.Connection connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.
        """
        self._channel = None
        if self._closing and self._connection:
            self._connection.ioloop.stop()
        else:
            self.logger.warning("Connection closed, reconnect necessary: %s", reason)
            self.reconnect()

    def reconnect(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.
        """
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.
        """
        self.logger.info("Creating a new channel")
        if self._connection:
            self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.
        Since the channel is now open, we'll declare the exchange to use.
        :param pika.channel.Channel channel: The channel object
        """
        self.logger.info("Channel opened")
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.parameters.get("EXCHANGE"))

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """
        self.logger.info("Adding channel close callback")
        if self._channel:
            self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.
        :param pika.channel.Channel: The closed channel
        :param Exception reason: why the channel was closed
        """
        self.logger.warning("Channel %i was closed: %s", channel, reason)
        self.close_connection()

    def setup_exchange(self, exchange_name) -> None:
        """Setup the exchange on RabbitMQ bfy invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.
        :param str|unicode exchange_name: The name of the exchange to declare
        """
        self.logger.info("Declaring exchange: %s", exchange_name)
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        cb = functools.partial(self.on_exchange_declareok, userdata=exchange_name)
        if self._channel:
            self._channel.exchange_declare(
                durable=True,
                exchange=exchange_name,
                exchange_type=self.parameters.get("EXCHANGE_TYPE"),
                callback=cb,
            )

    def on_exchange_declareok(self, _unused_frame, userdata):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.
        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame
        :param str|unicode userdata: Extra user data (exchange name)
        """
        self.logger.info("Exchange declared: %s", userdata)
        self.setup_queue(self.parameters.get("QUEUES"))

    def setup_queue(self, queues: List[str]):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.
        """
        for queue in queues:
            self.logger.info("Declaring queue %s", queue)
            cb = functools.partial(self.on_queue_declareok, userdata=queue)
            if self._channel:
                self._channel.queue_declare(queue=queue, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.
        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        queue_name = userdata
        self.logger.info(
            "Binding %s to %s with %s",
            self.parameters.get("EXCHANGE"),
            queue_name,
            self.parameters.get("ROUTING_KEY"),
        )
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        if self._channel:
            for routing_key in self.parameters.get("ROUTING_KEY").split(","):
                self._channel.queue_bind(
                    queue_name,
                    self.parameters.get("EXCHANGE"),
                    routing_key=routing_key,
                    callback=cb,
                )

    def on_bindok(self, _unused_frame, userdata):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will set the prefetch count for the channel.
        :param pika.frame.Method _unused_frame: The Queue.BindOk response frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        self.logger.info("Queue bound: %s", userdata)
        self.set_qos()

    def set_qos(self):
        """This method sets up the consumer prefetch to only be delivered
        one message at a time. The consumer must acknowledge this message
        before RabbitMQ will deliver another one. You should experiment
        with different prefetch values to achieve desired performance.
        """
        if self._channel:
            self._channel.basic_qos(
                prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok
            )

    def on_basic_qos_ok(self, _unused_frame):
        """Invoked by pika when the Basic.QoS method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.
        :param pika.frame.Method _unused_frame: The Basic.QosOk response frame
        """
        self.logger.info("QOS set to: %d", self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.
        """
        self.logger.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        for queue in self.parameters.get("QUEUES"):
            if self._channel:
                self._consumer_tags.append(
                    self._channel.basic_consume(queue, self.on_message)
                )
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.
        """
        self.logger.info("Adding consumer cancellation callback")
        if self._channel:
            self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.
        :param pika.frame.Method method_frame: The Basic.Cancel frame
        """
        self.logger.info(
            "Consumer was cancelled remotely, shutting down: %r", method_frame
        )
        if self._channel:
            self._channel.close()

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.
        :param int delivery_tag: The delivery tag from the Basic.Deliver frame
        """
        self.logger.info("Acknowledging message %s", delivery_tag)
        if self._channel:
            self._channel.basic_ack(delivery_tag)

    def unacknowledge_message(self, delivery_tag, **kwargs):
        if self._channel:
            self._channel.basic_nack(delivery_tag, **kwargs)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        """
        if self._channel:
            self.logger.info("Sending a Basic.Cancel RPC command to RabbitMQ")
            for tag in self._consumer_tags:
                cb = functools.partial(self.on_cancelok, userdata=tag)
                self._channel.basic_cancel(tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.
        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)
        """
        self._consuming = False
        self.logger.info(
            "RabbitMQ acknowledged the cancellation of the consumer: %s", userdata
        )
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """
        self.logger.info("Closing the channel")
        if self._channel:
            self._channel.close()

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.
        """
        self.logger.info("Run")
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.
        """
        if not self._closing and self._connection:
            self._closing = True
            self.logger.info("Stopping")
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            self.logger.info("Stopped")


class ReconnectingConsumer:
    def __init__(self, parameters):
        self.__parameters = parameters
        self._reconnect_delay = 0
        self._consumer = BaseConsumer(
            self.__parameters, self.on_message, current_logger=logger
        )

    def on_message(
        self,
        _unused_channel: pika.channel.Channel,
        basic_deliver: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ):
        pass

    def consume(self):
        while True:
            try:
                self._consumer.run()
            except KeyboardInterrupt:
                self._consumer.stop()
                break
            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self._consumer.should_reconnect:
            self._consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            logger.info("Reconnecting after %d seconds", reconnect_delay)
            time.sleep(reconnect_delay)
            self._consumer = BaseConsumer(
                self.__parameters, self.on_message, current_logger=logger
            )

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay
