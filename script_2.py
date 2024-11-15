import requests

from user_agent import generate_user_agent


class Bot:
    HOST = 'https://zakupki.mos.ru/ru'

    def __init__(self, authorization, login, url, min_price):
        self.headers = {'user-agent': generate_user_agent(), 'authority': 'old.zakupki.mos.ru', 'scheme': 'https',
                        'accept': 'application/json, text/plain, */*', 'content-type': 'application/json',
                        'authorization': authorization, 'referer': url}
        self.session = requests.Session()
        self.session.get(self.HOST)
        self.session.headers.update(self.headers)
        self.login = login
        self.url = url
        self.id_tender = int(url.split('/')[-1])
        self.min_price = int(min_price)
        self.sing_up()

    def sing_up(self):
        self.session.get('https://zakupki.mos.ru/Api/Cssp/JsApi/GetKeycloakSettings')
        self.session.get('https://zakupki.mos.ru/Api/Cssp/JsApi/GetJsSettings')
        self.session.get('https://old.zakupki.mos.ru/api/Cssp/Authentication/CheckAuthentication')
        self.session.headers.update({'x-xsrf-token': self.session.cookies.get('XSRF-TOKEN'),
                                     'cookie': self.session.cookies.get('session-cookie'),
                                     'referer': f'https://zakupki.mos.ru/auction/{self.id_tender}',
                                     'pp_uid_v2': f'{self.login.split("@")[0]}%40yandex.ru'})
        self.session.post('https://zakupki.mos.ru/auth/realms/PpRealm/login-actions/authenticate?'
                          'session_code=vrsfCAj2hXd4dLXTDgsMGFa2TVbTk4OGu-b9XS-KKEs&'
                          'execution=e0da673b-49ed-4a1b-aaa5-83d77e6a0fa0&'
                          'client_id=PpApp&'
                          'tab_id=N_BMcQ2LesA', json={'username': self.login, 'password': 'Timsongeroup123'})

    def work_constant(self):
        try:
            info_bet = self.session.get(f'https://zakupki.mos.ru/newapi/api/Auction/Get?'
                                        f'auctionId={self.id_tender}').json()
            if info_bet['nextCost'] >= self.min_price:
                create_bet = self.session.post('https://zakupki.mos.ru/newapi/api/AuctionBets/CreateBet',
                                               json={'auctionId': self.id_tender,
                                                     'value': info_bet['nextCost'],
                                                     'rowVersion': info_bet['rowVersion']})
                if create_bet.status_code <= 204:
                    print(f'Ставка сделана! Статус: {create_bet.status_code}')
                try:
                    print(f'Последнюю ставку сделал: {info_bet["lastBet"]["supplier"]["name"]}')
                except Exception:
                    pass
            else:
                return False
        except Exception as ex:
            print(f'Ошибка! {ex}')


def work_function_2(authorization, auction_url, min_price):
    bot_object = Bot(authorization, 'svezhentsovttt@gmail.com', auction_url, min_price)
    func = bot_object.work_constant
    while True:
        if not func():
            return f'Бот ИП Свеженцов закончил работу'
