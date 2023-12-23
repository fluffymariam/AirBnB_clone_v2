#!/usr/bin/python3
"""This is the state class"""
import shlex
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel, Base
import models
from models.city import City


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City",
        cascade='all, delete, delete-orphan',
        backref="state"
    )

    @property
    def cities(self):
        all_models = models.storage.all()
        cities_list = [
            model for model in all_models.values() if isinstance(model, City)
        ]
        matching_cities = [
            city for city in cities_list if city.state_id == self.id
        ]
        return matching_cities
