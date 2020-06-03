import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "casting"
    database_path = "postgres://{}:{}@{}/{}".format('postgres','password','localhost:5432', database_name)
# set DATABASE_URL = "postgres://postgres:password@localhost:5432/casting"
db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    print(database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    db.create_all()

'''
Schedule

'''
class Schedule(db.Model):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key = True)
    actor_id =  Column(Integer, db.ForeignKey("actor.id",ondelete='CASCADE'))
    movie_id = Column(Integer, db.ForeignKey("movie.id",ondelete='CASCADE'))
    start = Column(db.Date, nullable=True)
    end = Column(db.Date, nullable=True)


'''
Actor

'''
class Actor(db.Model):
    __tablename__ = "actor"
    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender,
        }

'''
Category

'''
class Movie(db.Model):
    __tablename__ = "movie"
    id = Column(Integer, primary_key = True)
    title = Column(String(64), nullable=False)
    desc =  Column(String(500), nullable=True)
    release_date = Column(db.DateTime, nullable=True,
        default=datetime.utcnow)
    actors = db.relationship("Actor",
            secondary="schedule",
            backref=db.backref("movies", lazy="dynamic"),
            )

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'desc': self.desc,
        'release_date': self.release_date
        }