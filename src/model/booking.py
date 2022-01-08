from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, DateTime

from model.base import Base, db
from model.booking_status import BookingStatus
from model.item import Item


class Booking(Base, db.Model):
    __tablename__ = "booking"
    discount = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status_id = Column(Integer, ForeignKey("booking_status.id", ondelete="CASCADE"), nullable=True)

    item_id = Column(Integer, ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    order_bookings = relationship("OrderBookings", backref="booking")

    def __init__(self, discount, location, start_time, end_time, status_id, item_id):
        self.discount = discount
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.status_id = status_id
        self.item_id = item_id

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
    def get_bookings_by_item_id(cls, item_id):
        active_id = BookingStatus.get_id_by_name("Active")
        return cls.query.filter(cls.item_id == item_id, cls.status_id == active_id).all()

    @classmethod
    def close_booking(cls, booking_id):
        closed_id = BookingStatus.get_id_by_name("Closed")
        cls.query.filter(cls.id == booking_id).update({"status_id": closed_id})
        db.session.commit()

    @classmethod
    def getQuery_BookingByItemType(cls, item_type_id):
        bookings = db.session.query(Booking).join(
            Item).filter(Item.item_type_id == item_type_id).group_by(Booking)
        return bookings
