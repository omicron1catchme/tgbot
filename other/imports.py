from dateutil import relativedelta
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime

from other.database import Database
from other.states import StatusStatus, CaptchaStatus
from other.VK_api import CaptchaHandler, Account, VerifyAccount
from other.keyboards import TXTKeyboard
from aiogram.dispatcher.filters.state import StatesGroup, State