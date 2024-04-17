from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from aiogram_dialog.api.exceptions import NoContextError
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.input.text import TextInput

from oac.My_token import TOKEN, ADMIN_ID


bot = Bot(TOKEN)


async def del_message(event: CallbackQuery | Message) -> None:
    user_id = event.from_user.id
    match event:
        case CallbackQuery() as c:
            await bot.delete_message(user_id, c.message.message_id)
        case Message() as m:
            await bot.delete_message(user_id, m.message_id-1)


async def on_asking(m: Message,
                    w: TextInput,
                    dm: DialogManager,
                    input_data: str,
                    **kwargs) -> None:

    await del_message(m)
    text = f'@{m.from_user.username}:\n{input_data}'
    await m.answer('Спасибо. Сообщение отправлено')
    await bot.send_message(ADMIN_ID, text)
    await dm.done()


async def on_del_window(c: CallbackQuery,
                        w: Cancel,
                        dm: DialogManager,
                        **kwargs) -> None:
    await del_message(c)
    await dm.done()
