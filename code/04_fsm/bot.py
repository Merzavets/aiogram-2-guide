from os import path 
    
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
# from app.handlers.drinks import register_handlers_drinks
from app.handlers.food import register_handlers_food
from app.handlers.search import register_handlers_search
from app.handlers.common import register_handlers_common

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/drinks", description="Заказать напитки"),
        BotCommand(command="/search", description="Поискать детишек"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    
    file_path = path.dirname(path.realpath(__file__))

    # Парсинг файла конфигурации
    config = load_config(file_path + '/config/bot.ini')
    

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token = config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp, config.tg_bot.admin_id)
    # register_handlers_drinks(dp)
    register_handlers_search(dp)
    register_handlers_food(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
