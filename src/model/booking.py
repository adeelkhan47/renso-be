import datetime

from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer

from model.base import Base, db
from model.booking_status import BookingStatus
from model.item import Item


class Booking(Base, db.Model):
    __tablename__ = "booking"
    cost = Column(Float, default=0)
    cost_without_tax = Column(Float, default=0, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    booking_status_id = Column(Integer, ForeignKey("booking_status.id", ondelete="SET NULL"), nullable=True)
    item_id = Column(Integer, ForeignKey("item.id", ondelete="SET NULL"), nullable=False)
    order_bookings = relationship("OrderBookings", backref="booking")
    cart_bookings = relationship("CartBookings", backref="booking")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("location.id", ondelete="SET NULL"), nullable=False, index=True)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))

    def __init__(self, start_time, end_time, booking_status_id, item_id, cost, cost_without_tax, user_id, location_id):
        self.start_time = start_time
        self.end_time = end_time
        self.booking_status_id = booking_status_id
        self.item_id = item_id
        self.cost = cost
        self.cost_without_tax = cost_without_tax
        self.user_id = user_id
        self.location_id = location_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def update(cls, id, data, session=None):
        if not session:
            session = db.session
        session.query(cls).filter(cls.id == id).update(data)
        session.commit()

    @classmethod
    def delete_pending_bookings(cls, session=None):
        if not session:
            session = db.session
        pending_id = BookingStatus.get_id_by_name("Pending", session)
        start_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
        session.query(cls).filter(cls.booking_status_id == pending_id, cls.created_at < start_time).delete()
        session.commit()

    @classmethod
    def get_bookings_by_item_id(cls, item_id):
        active_id = BookingStatus.get_id_by_name("Active")
        pending_id = BookingStatus.get_id_by_name("Pending")
        payment_pending_id = BookingStatus.get_id_by_name("Payment Pending")
        return cls.query.filter(cls.item_id == item_id, cls.is_deleted == False,
                                cls.booking_status_id.in_((active_id, payment_pending_id, pending_id))).all()

    @classmethod
    def get_confirmed_bookings_by_item_id(cls, item_id):
        active_id = BookingStatus.get_id_by_name("Active")
        payment_pending_id = BookingStatus.get_id_by_name("Payment Pending")
        return cls.query.filter(cls.item_id == item_id, cls.is_deleted == False,
                                cls.booking_status_id.in_((active_id, payment_pending_id))).all()

    @classmethod
    def close_booking(cls, booking_id, session=None):
        if not session:
            session = db.session
        closed_id = BookingStatus.get_id_by_name("Closed", session)
        session.query(cls).filter(cls.id == booking_id).update({"booking_status_id": closed_id})
        db.session.commit()

    @classmethod
    def cancel_booking(cls, booking_id):
        closed_id = BookingStatus.get_id_by_name("Cancelled")
        cls.query.filter(cls.id == booking_id).update({"booking_status_id": closed_id})
        db.session.commit()

    @classmethod
    def getQuery_BookingByItemType(cls, item_type_id):
        bookings = db.session.query(Booking).join(
            Item).filter(Item.item_type_id == item_type_id).group_by(Booking)
        return bookings

    @classmethod
    def getQuery_BookingByItemSubType(cls, item_subtype_id):
        bookings = db.session.query(Booking).join(
            Item).filter(Item.item_subtype_id == item_subtype_id).group_by(Booking)
        return bookings
