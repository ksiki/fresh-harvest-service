from bot.create_bot import bot


async def send_notify(tg_id: int, message: str):
    await bot.send_message(chat_id=tg_id, text=message)
