from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class Location(Base, db.Model):
    __tablename__ = "location"
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price_factor = Column(Integer, nullable=False, default=100)
    item_locations = relationship("ItemLocation", backref="location")

    def __init__(self, name, description, price_factor):
        self.name = name
        self.description = description
        self.price_factor = price_factor

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()
