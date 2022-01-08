from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class BookingStatus(Base, db.Model):
    __tablename__ = "booking_status"
    name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=False)
    booking_status = relationship("Booking", backref="booking_status")

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def get_id_by_name(cls, name: str):
        row = db.session.query(cls).filter_by(name=name).first()
        return row.id
