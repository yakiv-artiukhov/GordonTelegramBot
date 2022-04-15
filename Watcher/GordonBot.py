
from  os import environ
from dotenv import load_dotenv
from aiogram import Bot



class GordonBot:
    def __init__(self) -> None:
        self.MY_CHAT_ID = '1041037404'
        
        load_dotenv()
        self.bot = Bot(environ.get('GORDON_BOT_TOKEN'))

    async def send_message(self, chat_id, message_text):
        await self.bot.send_message(chat_id, message_text)