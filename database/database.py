from database.models import db, Auction

with db:
    db.create_tables([Auction])
    print('DB online')


def create_auction(auction):
    try:
        Auction.get(Auction.id == auction['id'])
        return False
    except Exception:
        Auction.create(id=auction['id'],
                       name=auction['name'],
                       name_organization=auction['name_organization'],
                       start_price=auction['start_price'],
                       begin_date=auction['begin_date'],
                       end_date=auction['end_date'],
                       federal_law_name=auction['federal_law_name']).save()
        return True


def get_auction(id_auction):
    auction = Auction.get(Auction.id == id_auction)
    return auction.name, auction.name_organization, auction.start_price, auction.begin_date, \
           auction.end_date, auction.federal_law_name, auction.id
