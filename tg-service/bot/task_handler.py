from create_bot import bot

from shared.enums.task import TaskType
from shared.queue.broker import broker


@broker.task(task_name=TaskType.NOTIFY_USER)
async def send_notify(tg_id: int, message: str):
    await bot.send_message(chat_id=tg_id, text=message)
