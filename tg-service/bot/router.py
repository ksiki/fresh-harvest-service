from typing import Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import settings

router: Final[Router] = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🗾 Открыть карту",
            web_app=WebAppInfo(url=settings.web_app_url),
        )
    )

    await message.answer(
        "Добро пожаловать! Нажмите на кнопку ниже, чтобы открыть карту:",
        reply_markup=builder.as_markup(),
    )
