import logging
from  os import environ
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types



        
load_dotenv()

bot = Bot(environ.get('GORDON_BOT_TOKEN'))
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="track")
async def cmd_track(message: types.Message):
    await message.answer("Starting tracking Gordon news!")




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

