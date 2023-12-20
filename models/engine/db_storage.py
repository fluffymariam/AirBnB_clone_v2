#!/usr/bin/python3
"""creates a new class"""
import models
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage:
    """create tables"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(getenv('HBNB_MYSQL_USER'),getenv('HBNB_MYSQL_PWD'), getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
    def all(self, cls=None):
        """Returns an object"""
        my_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            inc = self.__session.query(cls)
            for element in inc:
                key = "{}.{}".format(type(element).__name__, element.id)
                my_dict[key] = element
            else:
                my_list = [State, City, User, Place, Review, Amenity]
                for i in my_list:
                    inqury = self.__session.query(i)
                    for j in inqury:
                        key = "{}.{}".format(type(j).__name__, j.id)
                        my_dict[key] = j
        return my_dict

    def new(self, obj):
        """add element"""
        self.__session.add(obj)

    def save(self):
        """save"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete element"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload"""
        Base.metadata.create_all(self.__engine)
        sess_maker = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_maker)
        self.__session = Session()

    def close(self):
        """close"""
        self.__session.close()
