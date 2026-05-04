import logging
from typing import Final

from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from shared.queue.broker import broker

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger(__name__)


def get_scheduler() -> TaskiqScheduler:
    try:
        logger.info("Initializing TaskiqScheduler")

        sources = [LabelScheduleSource(broker)]
        scheduler = TaskiqScheduler(broker=broker, sources=sources)

        logger.info("Scheduler created successfully.")
        return scheduler
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {e}")
        raise


scheduler: Final[TaskiqScheduler] = get_scheduler()
