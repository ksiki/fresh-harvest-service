import logging
from typing import Final

from taskiq_aio_pika import AioPikaBroker

from shared.common_config import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger(__name__)


def get_broker(url: str) -> AioPikaBroker:
    try:
        logger.info("Initializing AioPikaBroker")

        broker = AioPikaBroker(url=url)

        logger.info("Broker created successfully.")
        return broker
    except Exception as e:
        logger.error(f"Failed to initialize broker: {e}")
        raise


broker: Final[AioPikaBroker] = get_broker(url=settings.rabbitmq_url)
