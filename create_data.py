# File Name: create_data.py

from sqlalchemy.orm import sessionmaker
from faker import Faker
from db import Base, engine, User, Course

session = sessionmaker(engine)()
fake = Faker('zh-cn')


def create_users():
    for i in range(10):
        user = User(name=fake.name(), email=fake.email())
        session.add(user)


def create_courses():
    for user in session.query(User).all():
        for i in range(2):
            course = Course(name=''.join(fake.words(4)), user_id=user.id)
            session.add(course)


def main():
    create_users()
    create_courses()
    session.commit()


if (__name__ == '__main__'):
    main()

