from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Float, Integer

from model.base import Base, db
from model.booking import Booking
from model.booking_status import BookingStatus
from model.item import Item
from model.order_bookings import OrderBookings


class Order(Base, db.Model):
    __tablename__ = "order"
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    time_period = Column(String, nullable=False)
    total_cost = Column(Float, nullable=False)
    order_status_id = Column(Integer, ForeignKey("order_status.id", ondelete="CASCADE"), nullable=True)

    order_bookings = relationship("OrderBookings", backref="order")

    def __init__(self, client_name, client_email, phone_number, order_status_id, time_period, total_cost):
        self.client_name = client_name
        self.client_email = client_email
        self.phone_number = phone_number
        self.order_status_id = order_status_id
        self.time_period = time_period
        self.total_cost = total_cost

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
    def getQuery_OrderByItemType(cls, item_type_id):
        orders = db.session.query(Order).join(OrderBookings).join(Booking).filter(
            OrderBookings.booking_id == Booking.id).join(
            Item).filter(Item.item_type_id == item_type_id).group_by(Order)
        return orders
