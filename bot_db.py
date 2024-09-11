from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, \
    DateTimeField, SQL

# connecting to database my_database.db
db = SqliteDatabase("my_database.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    # creating table User
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)
    language = CharField()


class History(BaseModel):
    # Creating table History
    user = ForeignKeyField(User, backref='history')
    command = CharField()
    pair = CharField()
    result = CharField()
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])


# creating table 'users' and 'history' in database
db.create_tables([User, History])
