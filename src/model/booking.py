from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db


class Booking(Base, db.Model):
    __tablename__ = "booking"
    discount = Column(Integer, nullable=False, unique=False)
    location = Column(String, nullable=False, unique=True)
    start_time = Column(String, nullable=False, unique=False)
    end_time = Column(String, nullable=False, unique=True)

    item_id = Column(Integer, ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    order_bookings = relationship("OrderBookings", backref="booking")

    def __init__(self, discount, location, start_time, end_time, item_id):
        self.discount = discount
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.item_id = item_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
