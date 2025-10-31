from aiogram.types import Message
from aiogram import Bot
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input.text import TextInput

from config_reader import config


async def on_click(m: Message,
                   w: TextInput,
                   dm: DialogManager,
                   input_data: str,
                   ** kwargs) -> None:

    bot = Bot(config.get_token())
    text = f'@{m.from_user.username}:\n{input_data}'
    await dm.event.answer('Спасибо. Сообщение отправлено')
    await bot.send_message(config.get_admin_id(), text)
    await dm.done()
