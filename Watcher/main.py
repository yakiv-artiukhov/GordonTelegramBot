
from GordonWatcher import GordonWatcher
from NewsRepository import NewsRepository

from os import environ
from time import sleep
from datetime import datetime
from dotenv import load_dotenv
from threading import Lock

from aiogram import Bot, Dispatcher, executor, types


lock = Lock()
news_repository = NewsRepository(lock)

load_dotenv()
bot = Bot(environ.get('GORDON_BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands="track")
async def cmd_track(message: types.Message):
    #print(message.from_user.id)
    await message.answer(f"Starting tracking Gordon news! User id: {message.from_user.id}")
    timestamp = datetime.now()
    while(True):
        untracked_news = news_repository.get_untracked_news(timestamp)
        if len(untracked_news) > 0:
            timestamp = datetime.now()
            for news in untracked_news:
                await message.answer(news._to_message_string())
        sleep(60)


def main():

    gw = GordonWatcher(news_repository)
    gw.start_watching()
    
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()