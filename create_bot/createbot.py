from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from aiogram.dispatcher import FSMContext

from telegram_token import TOKEN

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
