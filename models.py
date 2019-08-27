from flask_bcrypt import generate_password_hash
from peewee import *

DATABASE = SqliteDatabase("tacosocial.db")

class User(Model):
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
            raise ValueError("This email has already been used!")
        except ValueError as err:
            pass



class Taco(Model):
    PROTEIN_CHOICES = (
        ("chicken", "chicken"),
        ("beef", "beef"),
        ("fish", "fish")
    )
    SHELL_CHOICES = (
        ("hard", "hard"),
        ("soft", "soft")
    )
    user = ForeignKeyField(rel_model=User, related_name="tacos")
    protein = CharField(
        choices=PROTEIN_CHOICES, 
    )
    shell = CharField(
        choices=SHELL_CHOICES,
    )
    cheese = BooleanField()
    extras = CharField(max_length=100)

    class Meta:
        database = DATABASE



def initialize_database():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()