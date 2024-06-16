from other.imports import *
from create_bot.createbot import bot


db = Database(path_db_file='users.db')

captcha = CaptchaHandler()
acc_token = Account()


async def login_and_password(msg: types.Message):
    await msg.answer(text=f"""
{msg.from_user.first_name.capitalize()}, вот твои данные:""")
    await msg.answer(text=f"""
Логин: <tg-spoiler>{db.get_user_inf(user_id=msg.from_user.id)['login']}</tg-spoiler>
Пароль: <tg-spoiler>{db.get_user_inf(user_id=msg.from_user.id)['password']}</tg-spoiler>""",
                     parse_mode='HTML')


async def check_profile_vk(msg: types.Message, state: FSMContext):
    await msg.answer(text='Ожидайте...')
    token = db.get_user_inf(user_id=msg.from_user.id)['token']

    result = acc_token.get_user_inf(token=token)

    if result == 'captcha':
        await state.finish()
        await CaptchaStatus.captcha.set()
        login = db.get_user_inf(user_id=msg.from_user.id)["login"]
        password = db.get_user_inf(user_id=msg.from_user.id)["password"]

        response = captcha.get_captcha_inf(login=login, password=password)

        url = response['captcha']
        db.set_token(user_id=msg.from_user.id, access_token=response['sid'])

        await bot.send_photo(chat_id=msg.from_user.id, photo=url, caption='''
        Необходимо пройти капчу:
        Для этого нужно отправить то, что написано на фотографии
        ''', reply_markup=ReplyKeyboardRemove())
    elif result == 'spam':

        await msg.answer(text=r'''
Вы <i>слишком часто</i> пытаетесь просмотреть ваш профиль!
<b>Не нажимайте на кнопки слишком часто</b> или попробуйте позднее''', parse_mode='HTML')
    else:
        info = result[0]
        followers = result[1]['count']
        friends_req = result[2]
        new_messages = result[3]
        gifts = result[4]
        last_seen: relativedelta.relativedelta = result[5]
        await msg.answer_photo(caption=f"""
Ваш профиль ВК:

{info['first_name']} {info['last_name']}
День рождения: {info['bdate'] if info['bdate'] != '' else 'Нет даты рождения'}
Пол: {'Мужской' if info['sex'] == 2 else 'Женский'}

Сейчас: {'Онлайн' if info['online'] else f'Был в сети {str(last_seen.days) + "д. " if last_seen.days else ""}'
                                         f'{str(last_seen.hours) + "ч. " if last_seen.hours else ""}'
                                         f'{str(last_seen.minutes) + "м." if last_seen.minutes else ""} назад..'}  
О себе: {'Информация о себе отсутствует' if info['about'] == '' else info['about']}
Статус: {info['status'] if info['status'] else 'Отсутствует'}
<a href='https://vk.com/{info['screen_name']}'>Ссылка на страницу</a>

Друзей: {info['counters']['friends']}
Подписчиков: {followers}
Новые заявки в друзья: {friends_req}

Подарки: {gifts}

Новые сообщения: {new_messages}

        """, photo=result[0]['photo_max'], parse_mode='HTML')


# @dp.message_handler(commands='обновить_статус')
async def new_status(msg: types.Message):
    await msg.answer(text='Введите новый статус:', reply_markup=ReplyKeyboardRemove())
    await StatusStatus.status.set()



async def author(msg: types.Message):
    await msg.reply(text="""
<a href='tg://user?id=6858797803'>великий создатель созидатель</a>
""", parse_mode='HTML') #кто автор



# @dp.message_handler(commands='мои_подарки')
async def check_gifts(msg: types.Message, state: FSMContext):
    await msg.answer(text='Ожидайте...')
    token = db.get_user_inf(user_id=msg.from_user.id)['token']

    gifts = acc_token.get_user_gifts(token)

    user_id = msg.from_user.id

    if gifts == 'captcha':
        await state.finish()
        await CaptchaStatus.captcha.set()
        login = db.get_user_inf(user_id=user_id)["login"]
        password = db.get_user_inf(user_id=user_id)["password"]

        response = captcha.get_captcha_inf(login=login, password=password)

        url = response['captcha']
        db.set_token(user_id=msg.from_user.id, access_token=response['sid'])

        await bot.send_photo(chat_id=user_id, photo=url, caption='''
    Необходимо пройти капчу:
    Для этого нужно отправить то, что написано на фотографии
            ''', reply_markup=ReplyKeyboardRemove())
    elif gifts == 'spam':
        await msg.answer(text=r'''
Вы <i>слишком часто</i> пытаетесь просмотреть ваши подарки!
<b>Не нажимайте на кнопки слишком часто</b> или попробуйте позднее''', parse_mode='HTML')
    else:
        if len(gifts) <= 7:
            await msg.answer(text="Все подарки:")
        else:
            await msg.answer(text='Первые 7 подарков:')
            del gifts[7]
        for gift in gifts:
            await bot.send_photo(chat_id=user_id, photo=gift['photo'], parse_mode='HTML', caption=f"""
Oт кого: {f"<a href='{gift['url']}'>{gift['user']}</a>" if gift['url'] else gift['user']}
Дата: {' в '.join(str(datetime.fromtimestamp(gift['date'])).split())}
Заголовок: {gift['message'] if gift['message'] else '<a>Заголовок отсутствует</a>'}""")


def register_main_handler(dp: Dispatcher):
    dp.register_message_handler(login_and_password, commands='логин&пароль')
    dp.register_message_handler(check_profile_vk, commands='профиль_вк')
    dp.register_message_handler(new_status, commands='обновить_статус')
    dp.register_message_handler(check_gifts, commands='мои_подарки')
    dp.register_message_handler(author, commands="ктоавторэтогоговна")
