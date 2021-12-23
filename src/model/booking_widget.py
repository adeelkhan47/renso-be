from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Boolean

from model.base import Base, db


class BookingWidget(Base, db.Model):
    __tablename__ = "booking_widget"
    date_Picker = Column(Boolean, nullable=False, unique=True)
    time_Picker = Column(Boolean, nullable=False, unique=True)
    date_range_Picker = Column(Boolean, nullable=False, unique=True)

    def __init__(self, date_Picker, time_Picker, date_range_Picker):
        self.date_Picker = date_Picker
        self.time_Picker = time_Picker
        self.date_range_Picker = date_range_Picker

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
