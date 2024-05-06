from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from createbot import bot
from other.imports import *
from other.states import StatusReg, State, StatusStatus


db = Database(path_db_file='users.db')

verify_acc = VerifyAccount()
captcha = CaptchaHandler()
kb = TXTKeyboard()



async def start_bot(msg: types.Message):

    if not db.exists_user(user_id=msg.from_user.id):
        await msg.answer(text="<b>Привет! Чтобы войти в аккаунт VK нажми на /create</b>",
                         parse_mode='HTML',
                         reply_markup=kb.get_start_bot())

        await StatusReg.create.set()

        db.add_user(user_id=msg.from_user.id)
        await msg.delete()
    else:
        await msg.reply(text="<b>У вас уже есть профиль.\nЧтобы обновить его нажмите на /update</b>", parse_mode='HTML')
        await StatusReg.verify.set()



async def exit_red(msg: types.Message, state=FSMContext):
    if not (db.get_user_inf(user_id=msg.from_user.id)['token'] == '-'):
        await msg.answer(text='Редактирование отменено.', reply_markup=kb.main_kb())
        await msg.answer(text='Главное меню:')
        await state.finish()
    else:
        await msg.reply(text='Редактирование отменено.')
        await msg.answer(text="""
Чтобы <i>пройти аутентификацию в свой профиль</i> нажмите на <b>/verify</b>\n
Чтобы <i>посмотреть текущий логин и пароль</i> нажмите на <b>/show_info</b>\n
Чтобы <i>заново пройти регистрацию</i> нажмите на <b>/update</b>\n""", parse_mode='HTML', reply_markup=kb.verify_kb())
        await StatusReg.verify.set()


async def create_profile(msg: types.Message):
    db.set_token(user_id=msg.from_user.id, access_token='-')
    await msg.answer(text='Введите логин (почта или номер телефона формата +7XXXXXXXXXX)',
                     reply_markup=ReplyKeyboardRemove())
    await StatusReg.next()


async def not_login(msg: types.Message):
    await msg.reply(text=f'Это не логин!\nВведите логин заново.')


# @dp.message_handler(content_types='text', state=StatusReg.login)
async def write_login(msg: types.Message):
    if not msg.text.startswith('/') and (not ("'" in msg.text)) and (not ('"' in msg.text)) and (
            len(msg.text.split(' ')) == 1):
        db.set_login(user_id=msg.from_user.id, login=msg.text)
        await msg.answer(text='Введите пароль:')
        await msg.delete()
        await StatusReg.next()
    else:
        await msg.reply(text='Это не логин!\nВведите логин заново.')


async def not_password(msg: types.Message):
    await msg.reply(text=f'Это не пароль!\nВведите пароль заново.')


async def write_password(msg: types.Message):
    if not msg.text.startswith('/') and (not ("'" in msg.text)) and (not ('"' in msg.text)) and (
            len(msg.text.split(' ')) == 1):
        db.set_password(user_id=msg.from_user.id,
                        password=msg.text)
        await msg.answer(text='Регистрация прошла успешно!')  # dddd
        await msg.delete()
        await msg.answer(text="""
Чтобы <i>пройти аутентификацию в свой профиль</i> нажмите на <b>/verify</b>\n
Чтобы <i>посмотреть текущий логин и пароль</i> нажмите на <b>/show_info</b>\n
Чтобы <i>заново пройти регистрацию</i> нажмите на <b>/update</b>\n""", parse_mode='HTML',
                         reply_markup=kb.verify_kb())
        await StatusReg.next()
    else:
        await msg.reply(text='Это не пароль!\nВведите пароль заново.')


async def show_info(msg: types.Message, state=FSMContext):
    await msg.answer(text=f"""
{msg.from_user.first_name.capitalize()}, вот твои данные:""")
    await msg.answer(text=f"""
Логин: <tg-spoiler>{db.get_user_inf(user_id=msg.from_user.id)['login']}</tg-spoiler>
Пароль: <tg-spoiler>{db.get_user_inf(user_id=msg.from_user.id)['password']}</tg-spoiler>
""", parse_mode='HTML')


async def verification(msg: types.Message, state=FSMContext):
    user_id = msg.from_user.id

    login = db.get_user_inf(user_id=user_id)['login']
    password = db.get_user_inf(user_id=user_id)['password']

    result = verify_acc.verify_account(login=login, password=password)

    await msg.answer(text='Ожидайте...')

    if isinstance(result, tuple):
        token = result[1]

        db.set_token(user_id=user_id, access_token=token)
        await state.finish()

        await msg.answer(text='Аутентификация прошла успешно!')
        await msg.answer(text='Главное меню:', reply_markup=kb.main_kb())


    elif result == 'bad_password':
        await msg.answer(
            text='Ошибка аутентификации <u>(неправильно набран логин или пароль)</u>. Пройдите регистрацию заново',
            parse_mode='HTML')
        await msg.answer(text="""
Чтобы <i>пройти аутентификацию в свой профиль</i> нажмите на <b>/verify</b>\n
Чтобы <i>посмотреть текущий логин и пароль</i> нажмите на <b>/show_info</b>\n
Чтобы <i>заново пройти регистрацию</i> нажмите на <b>/update</b>\n""", parse_mode='HTML')
    elif result == 'captcha':
        await state.finish()
        await CaptchaStatus.captcha.set()

        response = captcha.get_captcha_inf(login=login, password=password)
        url = response['captcha']
        db.set_token(user_id=user_id, access_token=response['sid'])

        await bot.send_photo(chat_id=msg.from_user.id, photo=url, caption='''
Необходимо пройти капчу:
Для этого нужно отправить то, что написано на фотографии
''', reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(text=f'{result}, {type(result)}')

async def update_profile(msg: types.Message):
    await msg.reply(text='Вы уверены что хотите обновить профиль?',
                    reply_markup=kb.get_choose_kb())
    await StatusReg.create.set()

async def emp_msg(msg: types.Message):
    await msg.answer(text="""
Чтобы <i>пройти аутентификацию в свой профиль</i> нажмите на <b>/verify</b>\n
Чтобы <i>посмотреть текущий логин и пароль</i> нажмите на <b>/show_info</b>\n
Чтобы <i>заново пройти регистрацию</i> нажмите на <b>/update</b>\n""", parse_mode='HTML')


def register_reg_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start', state='*')
    dp.register_message_handler(exit_red, Text(equals='❌'), state=StatusReg.create)
    dp.register_message_handler(create_profile, Text(equals=['/create', '✅']), state=StatusReg.create)
    dp.register_message_handler(not_login,
                                content_types=['audio', 'document', 'sticker', 'contact', 'location', 'game', 'photo',
                                               'video', 'voice', 'video_note'], state=StatusReg.login)
    dp.register_message_handler(write_login, content_types='text', state=StatusReg.login)
    dp.register_message_handler(not_password,
                                content_types=['audio', 'document', 'sticker', 'contact', 'location', 'game', 'photo',
                                               'video', 'voice', 'video_note'], state=StatusReg.password)
    dp.register_message_handler(write_password, content_types='text', state=StatusReg.password)
    dp.register_message_handler(update_profile, commands=['update', 'обновить_данные'], state='*')
    dp.register_message_handler(show_info, commands='show_info', state=StatusReg.verify)
    dp.register_message_handler(verification, commands=['verify'], state=StatusReg.verify)

    dp.register_message_handler(emp_msg, state=StatusReg.verify)

