from sqlalchemy import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Date

from model.base import Base, db


class RestrictedDates(Base, db.Model):
    __tablename__ = "restricted_dates"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="SET NULL"), nullable=False, index=True,
                          unique=False)

    def __init__(self, start_date, end_date, item_type_id):
        self.start_date = start_date
        self.end_date = end_date
        self.item_type_id = item_type_id

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

    @classmethod
    def get_by_item_type_id(cls, item_type_id):
        return cls.query.filter(cls.item_type_id == item_type_id).first()

    @classmethod
    def validate_booking_date(cls, item_type_id, date):
        entry = db.session.query(cls).filter(cls.item_type_id == item_type_id, cls.start_date <= date,
                                                      cls.end_date >= date).first()
        if entry:
            return False
        return True
