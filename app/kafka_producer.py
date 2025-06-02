from aiokafka import AIOKafkaProducer
import json
import os
from datetime import datetime


class KafkaProducer:
    def __init__(self):
        self.bootstrap_servers = os.environ.get(
            "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
        )
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, message: dict):
        if not self.producer:
            await self.start()

        await self.producer.send(topic, message)


kafka_producer = KafkaProducer()


async def publish_user_registered_event(user_data: dict):
    """publish user registration event to kafka"""

    await kafka_producer.send_message(
        "user-registered",
        {
            "event_type": "user_registered",
            "user_id": user_data["user_id"],
            "email": user_data["email"],
            "name": user_data["name"],
            "timestamp": datetime.utcnow().isoformat(),
        },
    )
