from aiogram.dispatcher.filters.state import StatesGroup, State


class StatusReg(StatesGroup):
    create = State()
    login = State()
    password = State()
    verify = State()


class CaptchaStatus(StatesGroup):
    captcha = State()


class StatusStatus(StatesGroup):
    status = State()
