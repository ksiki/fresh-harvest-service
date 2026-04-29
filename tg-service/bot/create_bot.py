import logging
from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings

log_level = logging.DEBUG if settings.debug else logging.ERROR
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

storage: Final[MemoryStorage] = MemoryStorage()
dispatcher: Final[Dispatcher] = Dispatcher(storage=storage)
bot: Final[Bot] = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
