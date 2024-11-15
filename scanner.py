import requests

from database.database import create_auction


def scanner():
    try:
        response = requests.get(
            '''https://old.zakupki.mos.ru/api/Cssp/Purchase/Query?queryDto=%7B%22filter%22%3A%7B%22typeIn%22%3A%5B1%5D%2C%22nameLike%22%3A%22%D1%83%D1%82%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%2C%20%D1%83%D0%BD%D0%B8%D1%87%D1%82%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%2C%20%D0%B2%D1%8B%D0%B2%D0%BE%D0%B7%2C%20%D0%BE%D1%82%D1%85%D0%BE%D0%B4%D1%8B%2C%20%D0%BE%D0%B1%D1%80%D0%B0%D1%89%D0%B5%D0%BD%D0%B8%D0%B5%2C%20%D0%B2%D1%8B%D0%B7%D1%8B%D1%81%D0%BA%D0%B0%D0%BD%D0%B8%D0%B5%2C%20%D0%BE%D0%B1%D1%80%D0%B0%D1%89%D0%B5%D0%BD%D0%B8%D1%8E%22%2C%22regionPaths%22%3A%5B%22.1.504.%22%5D%2C%22auctionSpecificFilter%22%3A%7B%22stateIdIn%22%3A%5B19000002%5D%7D%2C%22needSpecificFilter%22%3A%7B%7D%2C%22tenderSpecificFilter%22%3A%7B%7D%2C%22ptkrSpecificFilter%22%3A%7B%7D%7D%2C%22order%22%3A%5B%7B%22field%22%3A%22PublishDate%22%2C%22desc%22%3Atrue%7D%5D%2C%22withCount%22%3Atrue%2C%22take%22%3A10%2C%22skip%22%3A0%7D''',
            timeout=10)
        all_new = []
        for item in response.json()['items']:
            auction = {'id': item['auctionId'],
                       'name': item['name'],
                       'name_organization': item['customers'][0]['name'],
                       'start_price': item['startPrice'],
                       'begin_date': item['beginDate'],
                       'end_date': item['endDate'],
                       'federal_law_name': item['federalLawName']}
            if create_auction(auction):
                all_new.append(f'Наименование: <b>{item["name"]}</b>\n\n'
                               f'Организация: <b>{item["customers"][0]["name"]}</b>\n\n'
                               f'Начальная цена: <b>{item["startPrice"]}</b>\n\n'
                               f'Дата начала: <b>{item["beginDate"]}</b>\n\n'
                               f'Дата окончания: <b>{item["endDate"]}</b>\n\n'
                               f'ФЗ: <b>{item["federalLawName"]}</b>\n\n'
                               f'Ссылка: https://zakupki.mos.ru/auction/{item["auctionId"]}')
        return all_new
    except Exception as e:
        print(e)
        return 'Error'
