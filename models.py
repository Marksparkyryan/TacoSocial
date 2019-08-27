from flask_bcrypt import generate_password_hash 
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase("tacosocial.db")

class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
    
    @classmethod
    def create_user(cls, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                )
        except IntegrityError:
            raise ValueError("Duplicate user error!")



class Taco(Model):
    user = ForeignKeyField(rel_model=User, related_name="tacos")
    protein = CharField()
    shell = CharField()
    cheese = BooleanField()
    extras = CharField(max_length=100)

    class Meta:
        database = DATABASE



def initialize_database():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()