import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

from app.core.config import settings
from app.models.events import ResumeUploadedEvent
from app.services.resume_service import resume_service

logger = logging.getLogger(__name__)


async def start_consumer() -> None:
    """
    Long-running async task. Started once in main.py lifespan.
    Reconnects automatically on Kafka connection loss.
    """
    while True:
        try:
            await _run_consumer_loop()
        except KafkaConnectionError as exc:
            logger.error("Kafka connection lost: %s — retrying in 5s", exc)
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled — shutting down")
            raise
        except Exception as exc:
            logger.error("Unexpected consumer error: %s — retrying in 5s", exc, exc_info=True)
            await asyncio.sleep(5)


async def _run_consumer_loop() -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    consumer = AIOKafkaConsumer(
        settings.KAFKA_RESUME_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    await producer.start()
    await consumer.start()
    logger.info("Consumer listening on topic: %s", settings.KAFKA_RESUME_TOPIC)

    try:
        async for message in consumer:
            await _handle_message(message, producer)
    finally:
        await consumer.stop()
        await producer.stop()


async def _handle_message(message, producer: AIOKafkaProducer) -> None:
    """
    Process one Kafka message.
    On failure: log the error and route to DLQ (Dead Letter Queue).

    DLQ = a separate Kafka topic that stores failed messages so they
    can be inspected and replayed later. Essential for production systems.
    """
    try:
        event = ResumeUploadedEvent(**message.value)
        logger.info("Processing event resumeId=%s user=%s", event.resumeId, event.userEmail)

        await resume_service.process(
            resume_id=event.resumeId,
            user_id=event.userId,
            user_email=event.userEmail,
            resume_text=event.resumeText,
            file_name=event.fileName,
        )

    except Exception as exc:
        logger.error(
            "Failed to process message, sending to DLQ. error=%s payload=%s",
            str(exc), message.value, exc_info=True,
        )
        await producer.send(settings.KAFKA_DLQ_TOPIC, message.value)