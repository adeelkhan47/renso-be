from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class OrderBookings(Base, db.Model):
    __tablename__ = "order_bookings"

    booking_id = Column(Integer, ForeignKey("booking.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, booking_id, order_id):
        self.booking_id = booking_id
        self.order_id = order_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_order_id(cls, order_id):
        cls.query.filter(cls.order_id == order_id).delete()
        db.session.commit()
