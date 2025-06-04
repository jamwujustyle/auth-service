from aiokafka import AIOKafkaProducer
import json
import os
from datetime import datetime, timezone
from .configs.logging_config import logger


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
        logger.critical(
            f'Kakfa producer started, connected to {os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")}'
        )

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, message: dict):
        if not self.producer:
            print("Kafka producer not available, skipping message")
            return
        try:
            await self.producer.send(topic, message)
            print(f"Message sent to topic {topic}")
        except Exception as ex:
            print(f"Failed to send message to Kafka: {ex}")


kafka_producer = KafkaProducer()


async def publish_user_registered_event(user_data: dict):
    """publish user registration event to kafka"""

    await kafka_producer.send_message(
        "user-registered",
        {
            "event_type": "user_registered",
            "user_id": user_data["id"],
            "email": user_data["email"],
            "name": user_data["name"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
