from peewee import SqliteDatabase, Model, IntegerField, TextField, FloatField

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Auction(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    name_organization = TextField()
    start_price = FloatField()
    end_date = TextField()
    begin_date = TextField()
    federal_law_name = TextField()

    class Meta:
        db_table = 'all_auctions'
