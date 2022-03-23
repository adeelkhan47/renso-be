from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class CartBookings(Base, db.Model):
    __tablename__ = "cart_bookings"

    booking_id = Column(Integer, ForeignKey("booking.id", ondelete="CASCADE"), nullable=False)
    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, booking_id, cart_id):
        self.booking_id = booking_id
        self.cart_id = cart_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_booking_id(cls, booking_id):
        cls.query.filter(cls.booking_id == booking_id).delete()
        db.session.commit()

    @classmethod
    def delete_by_cart_id(cls, cart_id):
        cls.query.filter(cls.cart_id == cart_id).delete()
        db.session.commit()

