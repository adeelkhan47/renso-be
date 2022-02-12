from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, DateTime

from model.base import Base, db


class Season(Base, db.Model):
    __tablename__ = "season"

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price_factor = Column(Integer, nullable=False, default=100)
    seasonItemTypes = relationship("SeasonItemTypes", backref="season")

    def __init__(self, start_time, end_time, price_factor):
        self.start_time = start_time
        self.end_time = end_time
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
