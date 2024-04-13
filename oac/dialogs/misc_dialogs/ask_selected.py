from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input.text import TextInput
from aiogram import Bot

from oac.My_token import TOKEN, ADMIN_ID


async def on_click(m: Message,
                   w: TextInput,
                   dm: DialogManager,
                   input_data: str,
                   ** kwargs) -> None:

    bot = Bot(TOKEN)
    text = f'@{m.from_user.username}:\n{input_data}'
    await dm.event.answer('Спасибо. Сообщение отправлено')
    await bot.send_message(ADMIN_ID, text)
    await dm.done()
