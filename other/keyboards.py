from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class TXTKeyboard:
    @staticmethod
    def get_start_bot() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='/create')]
        ], row_width=1, resize_keyboard=True)
        return kb

    @staticmethod
    def get_choose_kb() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='❌'), KeyboardButton(text='✅')],
        ], row_width=2, resize_keyboard=True)
        return kb

    @staticmethod
    def verify_kb() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='/show_info'), KeyboardButton(text='/update')],
            [KeyboardButton(text='/verify'), KeyboardButton(text="/ктоавторэтогоговна")]
        ], row_width=2, resize_keyboard=True)
        return kb

    # **************************************

    @staticmethod
    def main_kb() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='/обновить_данные'), KeyboardButton(text='/логин&пароль'),
             KeyboardButton(text='/профиль_вк')],
            [KeyboardButton(text='/мои_подарки'), KeyboardButton(text="/ктоавторэтогоговна")]
        ], row_width=3, resize_keyboard=True)
        return kb
