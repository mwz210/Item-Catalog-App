import sys

#SQL sqlalchemy imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#Password Hash Imports
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String(32), index=True)
    name = Column(String(250), nullable=False)
    password_hash = Column(String(250))
    picture = Column(String)
    email = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'id' : self.id,
        'name': self.name,
        'email': self.email,
        'picture': self.picture
        }

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    description = Column(String)
    item = relationship('Item', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name' : self.name,
            'id' : self.id,
            'description' : self.description
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    description = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name' : self.name,
            'id' : self.id,
            'description': self.description
        }

engine = create_engine('postgresql+psycopg2:///catalog')

Base.metadata.create_all(engine)
