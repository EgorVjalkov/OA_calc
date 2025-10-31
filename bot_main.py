import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from oac.bot import my_bot
from oac.dialogs import start_commands
from oac.dialogs.patient_dialog.windows import patient_dialog
from oac.dialogs.KES_dialog.KES_windows import KES_dialog
from oac.dialogs.misc_dialogs.misc_windows import feedback_dialog, theory_dialog

logging.basicConfig(level=logging.INFO)


async def main(bot: Bot):
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(start_commands.router)
    dp.include_router(patient_dialog)
    dp.include_router(KES_dialog)
    dp.include_router(feedback_dialog)
    dp.include_router(theory_dialog)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def bot_run():
    my_bot.mode = 'oac'
    bot = my_bot.get_bot()
    asyncio.run(main(bot))

def test_run():
    my_bot.mode = 'test'
    bot = my_bot.get_bot()
    asyncio.run(main(bot))


if __name__ == '__main__':
    test_run()
