#from PyQt5.QtCore.QByteArray import toUInt

from app import db
from app.models import User, Course, Enrolment
import datetime


def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'username': 'amy',   'email': 'amy@b.com', 'role': 'Admin', 'pw': 'amy.pw'},
        {'username': 'tom',   'email': 'tom@b.com',                  'pw': 'amy.pw'},
        {'username': 'yin',   'email': 'yin@b.com', 'role': 'Admin', 'pw': 'amy.pw'},
        {'username': 'tariq', 'email': 'trq@b.com',                  'pw': 'amy.pw'},
        {'username': 'jo',    'email': 'jo@b.com',                   'pw': 'amy.pw'}
    ]

    for u in users:
        # get the password value and remove it from the dict:
        pw = u.pop('pw')
        # create a new user object using the parameters defined by the remaining entries in the dict:
        user = User(**u)
        # set the password for the user object:
        user.set_password(pw)
        # add the newly created user object to the database session:
        db.session.add(user)

    courses = [
        {
            "title": "Creative Writing for Beginners",
            "description": "Explore the fundamentals of storytelling, character development, and creative expression in this introductory course.",
            "cost": 15000,
            "instructor": "Dr. Emily Carter",
        },
        {
            "title": "Starting Your Own Business",
            "description": "Learn the basics of entrepreneurship, business planning, and financial management to launch your own business.",
            "cost": 20000,
            "instructor": "Mark Johnson, MBA",
        },
        {
            "title": "Introduction to Python Programming",
            "description": "A beginner-friendly course covering Python syntax, data structures, and basic programming concepts.",
            "cost": 18000,
            "instructor": "Sarah Lin, M.S.",
            "prerequisites": "Basic computer literacy"
        },
        {
            "title": "Digital Photography Basics",
            "description": "Learn how to capture stunning digital photos, edit images, and understand camera settings.",
            "cost": 17500,
            "instructor": "Jason Rodriguez",
            "prerequisites": "Access to a digital camera"
        },
        {
            "title": "World History: Major Events & Movements",
            "description": "An exploration of significant historical events and social movements that shaped the modern world.",
            "cost": 16000,
            "instructor": "Dr. Laura Simmons",
        },
        {
            "title": "Mindfulness & Stress Management",
            "description": "Discover techniques for mindfulness, relaxation, and stress reduction to improve overall well-being.",
            "cost": 12000,
            "instructor": "Michelle Wong",
        },
        {
            "title": "Conversational Spanish for Beginners",
            "description": "Develop basic Spanish communication skills for everyday conversations and travel situations.",
            "cost": 14000,
            "instructor": "Carlos Fernández",
            "prerequisites": "None"
        },
        {
            "title": "Healthy Cooking on a Budget",
            "description": "Learn how to prepare nutritious and delicious meals while keeping costs low.",
            "cost": 13000,
            "instructor": "Chef Lisa Morgan",
            "prerequisites": "Basic kitchen equipment"
        }
    ]

    for c in courses:
        course = Course(**c)
        db.session.add(course)
    db.session.commit()