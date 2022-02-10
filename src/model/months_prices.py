from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class MonthsPrices(Base, db.Model):
    __tablename__ = "months_prices"
    January = Column(Integer, nullable=False, unique=True)
    February = Column(Integer, nullable=False, unique=True)
    March = Column(Integer, nullable=False, unique=True)
    April = Column(Integer, nullable=False, unique=True)
    May = Column(Integer, nullable=False, unique=True)
    June = Column(Integer, nullable=False, unique=True)
    July = Column(Integer, nullable=False, unique=True)
    August = Column(Integer, nullable=False, unique=True)
    September = Column(Integer, nullable=False, unique=True)
    October = Column(Integer, nullable=False, unique=True)
    November = Column(Integer, nullable=False, unique=True)
    December = Column(Integer, nullable=False, unique=True)

    def __init__(self, January, February, March, April, May, June, July, August, September, October, November,
                 December):
        self.January = January
        self.February = February
        self.March = March
        self.April = April
        self.May = May
        self.June = June
        self.July = July
        self.August = August
        self.September = September
        self.October = October
        self.November = November
        self.December = December

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
