from typing import List, Union, Callable
import traceback

import json
from confluent_kafka import Producer, Consumer, KafkaException

from svtools import SecureVisionTools as svt

log = svt.log


class KafkaHelper(object):
    def __init__(self, target_landscape='custom', config_section=None):
        self.kafka_config = {
            'bootstrap.servers': svt.conf.get('kafka', 'bootstrap_servers')
        }
        self.producer = None
        log.info("...")

    def publish(self, topic: str, message: Union[dict, str]) ->None:
        """

        :param topic:
        :param message:
        :return:
        """
        assert isinstance(message, str) or isinstance(message, dict)

        if not self.producer:
            self.producer = Producer(self.kafka_config)

        if isinstance(message, dict):
            message = json.dumps(message)

        # Asynchronous message producing
        self.producer.produce(topic, message.encode('utf-8'))


    def consume_forever(
        self,
        group_id: str,
        topics: List[str],
        callback_functions: List[Callable]
    ) -> None:
        """

        :param group_id:
        :param topics:
        :param callback_functions:
        :return:
        """
        assert len(topics) == len(callback_functions)
        callbacks = dict(zip(topics, callback_functions))
        self.kafka_config.update({
            'group.id': group_id,
            'session.timeout.ms': 5000,
            'auto.offset.reset': 'earliest'
        })
        c = Consumer(self.kafka_config, logger=svt.log, debug='fetch')
        c.subscribe(topics)
        # Read messages
        try:
            while True:
                message = c.poll(timeout=1.0)
                if not message:
                    log.info(
                        "There was no message on the subscribed Kafka topics!"
                    )
                elif message.error():
                    raise KafkaException(message.error())
                else:
                    message = json.loads(message.value().decode('utf-8'))
                    callbacks[message.topic()](message)

        except Exception as error:
            log.error(
                f"Unexpected event occured! Error: {traceback.format_exc()}"
            )
        finally:
            # Shut down the consumer to commit the current offsets
            c.close()