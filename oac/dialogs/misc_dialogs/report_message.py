from dataclasses import dataclass
from aiogram import Bot


@dataclass
class ReportMessage:
    user_id: int
    message_id: int
    bot: Bot

    async def send_n_pin(self, text: str = '', start_mode: bool = False):
        if start_mode:
            text = 'здесь будут отображаться данные пациента'
            await self.bot.send_message(self.user_id, text)
            await self.bot.pin_chat_message(self.user_id, self.message_id)
        else:
            await self.bot.edit_message_text(text, self.user_id, self.message_id)
