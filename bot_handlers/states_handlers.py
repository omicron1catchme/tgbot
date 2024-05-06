from createbot import bot
from other.imports import *
from other.states import StatusReg

db = Database(path_db_file='users.db')


acc_token = Account()
verify_acc = VerifyAccount()
captcha = CaptchaHandler()
kb = TXTKeyboard()


async def captcha_over(msg: types.Message, state: FSMContext):
    login = db.get_user_inf(user_id=msg.from_user.id)['login']
    password = db.get_user_inf(user_id=msg.from_user.id)['password']
    sid = db.get_user_inf(user_id=msg.from_user.id)['token']

    new_token = captcha.auth_over_with_captcha(login=login, password=password, sid=sid, captcha=msg.text)
    if 'username_or_password_is_incorrect' in list(new_token.values()):
        StatusReg.verify.set()
        await msg.reply(text='Вы успешно прошли капчу')
        await msg.answer(text="""
Чтобы <i>пройти аутентификацию в свой профиль</i> нажмите на <b>/verify</b>\n
Чтобы <i>посмотреть текущий логин и пароль</i> нажмите на <b>/show_info</b>\n
Чтобы <i>заново пройти регистрацию</i> нажмите на <b>/update</b>\n""", parse_mode='HTML')
    elif 'access_token' in new_token:
        db.set_token(user_id=msg.from_user.id, access_token=new_token['access_token'])
        await state.finish()
        await msg.reply(text='Вы успешно прошли капчу')
        await msg.answer(text='Главное меню', reply_markup=kb.main_kb())
    else:
        response = captcha.get_captcha_inf(login=login, password=password)
        url = response['captcha']
        db.set_token(user_id=msg.from_user.id, access_token=response['sid'])
        await msg.answer(text='Вы не прошли капчу.')
        await bot.send_photo(chat_id=msg.from_user.id, photo=url,
                             caption='''Отправьте то, что написано на фотографии...''',
                             reply_markup=ReplyKeyboardRemove())


async def status(msg: types.Message, state: FSMContext):
    token = db.get_user_inf(user_id=msg.from_user.id)["token"]


    response = acc_token.set_user_status(token=token, text=msg.text)

    if response == 'captcha':
        await state.finish()
        await CaptchaStatus.captcha.set()
        response = captcha.get_captcha_inf(login=login, password=password)

        url = response['captcha']
        db.set_token(user_id=msg.from_user.id, access_token=response['sid'])

        await bot.send_photo(chat_id=msg.from_user.id, photo=url, caption='''
Необходимо пройти капчу:
Для этого нужно отправить то, что написано на фотографии
        ''', reply_markup=ReplyKeyboardRemove())
    elif response == 'spam':
        await msg.answer(text='''Не отправляйте сообщения слишком часто.''')
    else:
        await msg.reply(text='Вы успешно обновили статус')
        await msg.answer(text='Главное меню:', reply_markup=kb.main_kb())
        await state.finish()


def register_states_handler(dp: Dispatcher):
    dp.register_message_handler(captcha_over, content_types='text', state=CaptchaStatus.captcha)
    dp.register_message_handler(status, content_types='text', state=StatusStatus.status)
