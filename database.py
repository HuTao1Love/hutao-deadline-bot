from peewee import Model, SqliteDatabase, BigIntegerField, TextField, DateField, CharField

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
    user = BigIntegerField(column_name="user", primary_key=True)
    subject = TextField(column_name="subject")
    task = TextField(column_name="task")
    deadline = DateField(column_name="deadline")
    time = CharField(column_name="time", max_length=11, null=True)  # formats: None, HH:MM, HH:MM-HH:MM

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
