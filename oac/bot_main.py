import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from oac.My_token import TOKEN
from oac.dialogs import commands
from oac.dialogs.windows import patient_dialog
from oac.dialogs.misc_dialogs.ask_window import feedback_dialog

logging.basicConfig(level=logging.INFO)


async def main():
    storage = MemoryStorage()
    bot = Bot(TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_router(commands.router)
    dp.include_router(patient_dialog)
    dp.include_router(feedback_dialog)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def bot_run():
    asyncio.run(main())


if __name__ == '__main__':
    bot_run()
