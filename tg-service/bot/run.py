import asyncio

from aiogram import Bot
from aiogram.types import MenuButtonWebApp, WebAppInfo
from config import settings
from create_bot import bot, dispatcher
from router import router


async def set_main_menu_button(bot: Bot):
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="🗾 Открыть карту",
            web_app=WebAppInfo(url=settings.web_app_url),
        )
    )


async def run():
    await bot.delete_webhook(drop_pending_updates=True)
    await set_main_menu_button(bot=bot)

    dispatcher.include_router(router=router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run())
