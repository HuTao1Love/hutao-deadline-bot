from peewee import Model, SqliteDatabase, BigIntegerField, TextField, DateField

db = SqliteDatabase('deadlines.sqlite')


def all_subclasses(base: type) -> list[type]:
    return [
        cls
        for sub in base.__subclasses__()
        for cls in [sub] + all_subclasses(sub)
    ]


class BaseModel(Model):
    class Meta:
        database = db


class Deadline(BaseModel):
    user = BigIntegerField(column_name="user")
    subject = TextField(column_name="subject")
    task = TextField(column_name="task")
    deadline = DateField(column_name="deadline")

    class Meta:
        table_name = 'deadlines'


class Subject(BaseModel):
    user = BigIntegerField(column_name="user")
    subject = TextField(column_name="subject")

    class Meta:
        table_name = 'subjects'


db.create_tables([
    sub for sub in all_subclasses(Model)
    if not sub.__name__.startswith('_')
])
