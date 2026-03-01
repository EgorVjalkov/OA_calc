import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config_reader import config
from oac.dialogs import start_commands
from oac.dialogs.patient_dialog.windows import patient_dialog
from oac.dialogs.KES_dialog.KES_windows import KES_dialog
from oac.dialogs.misc_dialogs.misc_windows import feedback_dialog, theory_dialog
from oac.dialogs.criteria_dialogs.criteria_windows import router as criteria_router

logging.basicConfig(level=logging.INFO)


async def main(bot: Bot):
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(start_commands.router)
    dp.include_router(patient_dialog)
    dp.include_router(KES_dialog)
    dp.include_router(feedback_dialog)
    dp.include_router(theory_dialog)
    dp.include_router(criteria_router)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def bot_run():
    token = config.get_token()
    bot = Bot(token)
    asyncio.run(main(bot))

if __name__ == '__main__':
    bot_run()
