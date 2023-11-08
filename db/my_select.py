from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Score, Subject, Teacher, Group

engine = create_engine('postgresql://user:123123@localhost/database')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    students = session.query(Student).all()
    top_students = []
    for student in students:
        average_score = session.query(func.avg(Score.score)).filter(Score.student_id == student.id).scalar()
        top_students.append((student, average_score))
    top_students = sorted(top_students, key=lambda x: x[1], reverse=True)[:5]
    return top_students

def select_2(subject_name):
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        return None
    scores = session.query(Score).filter(Score.subject_id == subject.id)
    students = [score.student for score in scores]
    top_student = None
    highest_average_score = 0
    for student in students:
        average_score = session.query(func.avg(Score.score)).filter(Score.student_id == student.id).scalar()
        if average_score > highest_average_score:
            highest_average_score = average_score
            top_student = student
    return top_student

def select_3(subject_name):
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        return None
    scores = session.query(Score.score).filter(Score.subject_id == subject.id)
    group_scores = {}
    for score in scores:
        student = score.student
        group_name = student.group.name
        if group_name not in group_scores:
            group_scores[group_name] = []
        group_scores[group_name].append(score.score)
    average_scores = {group_name: sum(scores) / len(scores) for group_name, scores in group_scores.items()}
    return average_scores

def select_4():
    average_score = session.query(func.avg(Score.score)).scalar()
    return average_score

def select_5(teacher_name):
    teacher = session.query(Teacher).filter(Teacher.name == teacher_name).first()
    if not teacher:
        return None
    subjects = session.query(Subject).filter(Subject.teacher_id == teacher.id).all()
    course_names = [subject.name for subject in subjects]
    return course_names

def select_6(group_name):
    group = session.query(Group).filter(Group.name == group_name).first()
    if not group:
        return None
    students = session.query(Student).filter(Student.group_id == group.id).all()
    student_names = [student.name for student in students]
    return student_names

def select_7(group_name, subject_name):
    group = session.query(Group).filter(Group.name == group_name).first()
    if not group:
        return None
    subject = session.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        return None
    scores = session.query(Score).filter(Score.subject_id == subject.id, Score.student.has(group_id=group.id))
    student_scores = {score.student.name: score.score for score in scores}
    return student_scores

def select_8(teacher_name):
    teacher = session.query(Teacher).filter(Teacher.name == teacher_name).first()
    if not teacher:
        return None
    subjects = session.query(Subject).filter(Subject.teacher_id == teacher.id).all()
    subject_ids = [subject.id for subject in subjects]
    scores = session.query(Score.score).filter(Score.subject_id.in_(subject_ids))
    average_score = session.query(func.avg(Score.score)).scalar()
    return average_score

def select_9(student_name):
    student = session.query(Student).filter(Student.name == student_name).first()
    if not student:
        return None
    subjects = session.query(Subject).join(Score).filter(Score.student_id == student.id)
    course_names = [subject.name for subject in subjects]
    return course_names

def select_10(student_name, teacher_name):
    student = session.query(Student).filter(Student.name == student_name).first()
    if not student:
        return None
    teacher = session.query(Teacher).filter(Teacher.name == teacher_name).first()
    if not teacher:
        return None
    subjects = session.query(Subject).join(Score).filter(Score.student_id == student.id, Subject.teacher_id == teacher.id)
    course_names = [subject.name for subject in subjects]
    return course_names
