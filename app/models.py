from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
import datetime

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal")
    enrolments = relationship("Enrolment", back_populates="user", cascade="all, delete-orphan")


    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    __tablename__ = 'courses'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128))
    description: so.Mapped[str] = so.mapped_column(sa.String(1024))
    cost: so.Mapped[int] = so.mapped_column()
    instructor: so.Mapped[str] = so.mapped_column(sa.String(128))
    prerequisites: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)
    enrolments: so.Mapped[list["Enrolment"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Enrolment(db.Model):
    __tablename__ = 'enrolments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    course_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("courses.id"))
    date_enroled: so.Mapped[datetime.datetime] = so.mapped_column(default=datetime.datetime.utcnow)
    user: so.Mapped["User"] = relationship(back_populates="enrolments")
    course: so.Mapped["Course"] = relationship(back_populates="enrolments")


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))