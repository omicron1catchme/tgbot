import json, requests, vk_api, time, dateutil.relativedelta
from vk_api.exceptions import Captcha as cpt, AuthError as spam
from datetime import datetime

class CaptchaHandler:

    @staticmethod
    def get_captcha_inf(login: str, password: str) -> dict[str, str]:
        # ПРИ УСЛОВИИ ЧТО ОШИБКА CAPTCHA
        session = requests.Session()

        params = {
            'grant_type': 'password',
            'client_id': '51814372',
            'client_secret': 'Vaf6OCuDmMGkj7iVocOG',
            'username': f'{login}',
            'password': f'{password}',
        }

        response = session.get(url='https://oauth.vk.com/token', params=params)

        return {'sid': json.loads(response.text)['captcha_sid'],
                'captcha': json.loads(response.text)['captcha_img']}

    @staticmethod
    def auth_over_with_captcha(login: str, password: str, sid, captcha):
        session = requests.Session()

        params = {
            'grant_type': 'password',
            'client_id': '51814372',
            'client_secret': 'Vaf6OCuDmMGkj7iVocOG',
            'username': f'{login}',
            'password': f'{password}',
            'captcha_sid': sid,
            'captcha_key': captcha
        }
        response = session.get(url='https://oauth.vk.com/token', params=params)
        print(json.loads(response.text))
        return json.loads(response.text)


class VerifyAccount:
    @staticmethod
    def verify_account(login: str, password: str) -> str:
        session = requests.Session()
        params = {
            'grant_type': 'password',
            'client_id': '51814372',
            'client_secret': 'Vaf6OCuDmMGkj7iVocOG',
            'username': f'{login}',
            'password': f'{password}',
        }
        response = json.loads(session.get(url='https://oauth.vk.com/token', params=params).text)

        if 'access_token' in response:
            return (False, response['access_token'])

        elif 'username_or_password_is_incorrect' in tuple(response.values()):
            return 'bad_password'

        elif 'captcha_sid' in response:
            return 'captcha'

        else:
            print(response)
            return 'cho'


class Account:
    @staticmethod
    def get_auth_status_token(token):
        session = vk_api.VkApi(token=token)
        try:
            session.get_api()
        except cpt:
            return 'captcha'
        except spam:
            return 'spam'
        except Exception as exc:
            print(exc)
        else:
            return session

    @classmethod
    def get_user_inf(cls, token, id=False):
        result = cls.get_auth_status_token(token=token)
        if result != 'spam' and result != 'captcha':
            if not id:
                try:
                    response = result.method(method='users.get', values={
                        'fields': 'bdate,sex,city,online,photo_max,screen_name,status,about,counters,last_seen'})
                    friends_messages = result.method(method='account.getCounters',
                                                     values={'filter': 'friends,messages'})

                    # frineds_olnline = result.method(method='friends.getOnline')

                    followers = result.method(method='users.getFollowers')
                    gifts = result.method(method='gifts.get')['count']

                    friends_req = friends_messages['friends']
                    new_messages = friends_messages['messages']


                    last_seen_unix = response[0]['last_seen']['time']

                    time_now = time.time()

                    date = datetime.fromtimestamp(last_seen_unix)
                    date_now = datetime.fromtimestamp(time_now)


                    last_seen = dateutil.relativedelta.relativedelta(date_now, date)
                except Exception as error:
                    ...
                    #print(error, 'ошибка', sep='\n')
                else:
                    return response[0], followers, friends_req, new_messages, gifts, last_seen
            else:
                try:
                    response = result.method(method='users.get', values={'user_ids': id, 'fields': 'bdate,sex,city,friends_status,online,photo_max,screen_name,about,status,last_seen'})
                    followers = result.method(method='users.getFollowers', values={'user_id': id})

                except Exception as error:
                    print(error, 'ошибка', result, sep='\n')
                else:
                    return response[0], followers
        else:
            print(result)
            return result

    @classmethod
    def get_user_gifts(cls, token):
        result = cls.get_auth_status_token(token=token)
        if result != 'spam' and result != 'captcha':
            try:
                response = result.method(method='gifts.get', values={'count': 8})
                gifts = []
                for gift in response['items']:
                    user_id = gift['from_id']
                    if user_id > 0:
                        user_info = result.method(method='users.get', values={'user_ids': user_id,
                                                                              'fields': 'screen_name'})[0]

                        user = f"{user_info['first_name']} {user_info['last_name']}"
                        url = f'https://vk.com/{user_info["screen_name"]}'
                    elif user_id < 0:
                        community = result.method(method='groups.getById', values={'group_id': abs(user_id)})[0]

                        user = f"{community['name']}"
                        url = f"https://vk.com/{community['screen_name']}"
                    else:
                        user = 'Неизвестный отправитель'
                        url = 0
                    gifts.append(
                        {
                            'date': gift['date'],
                            'user': user,
                            'photo': gift['gift']['thumb_256'],
                            'message': gift['message'],
                            'url': url
                        }
                    )
            except Exception as error:
                print(error, 'dfsdfs', gifts)
            else:
                return gifts
        else:
            return result

    @classmethod
    def set_user_status(cls, token, text):
        result = cls.get_auth_status_token(token=token)
        if result != 'spam' and result != 'captcha':
            try:
                response = result.method(method='status.set', values={'text': text})
            except Exception as error:
                print(error, 'ошибка', result, sep='\n')
            else:
                return 'done'
        else:
            return result



