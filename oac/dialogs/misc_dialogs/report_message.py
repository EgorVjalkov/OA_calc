from dataclasses import dataclass
from aiogram import Bot


@dataclass
class ReportMessage:
    user_id: int
    message_id: int
    bot: Bot

    async def edit(self, text: str):
        await self.bot.edit_message_text(text, self.user_id, self.message_id)

    async def del_rep_msg(self):
        await self.bot.delete_message(self.user_id, self.message_id)
