from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta

from models import Student, Group, Teacher, Subject, Score

engine = create_engine('postgresql://user:123123@localhost/database')

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

groups = [Group(name=fake.word()) for _ in range(3)]
teachers = [Teacher(name=fake.name()) for _ in range(5)]
subjects = [Subject(name=fake.word(), teacher=choice(teachers)) for _ in range(8)]

for _ in range(30):
    student = Student(name=fake.name(), group=choice(groups))
    session.add(student)
    for subject in subjects:
        score = Score(student=student, subject=subject, score=randint(1, 10), date=fake.date_between(start_date='-1y', end_date='today'))
        session.add(score)

session.commit()