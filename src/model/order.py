from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String

from model.base import Base, db
from model.booking import Booking
from model.item import Item
from model.order_bookings import OrderBookings


class Order(Base, db.Model):
    __tablename__ = "order"
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    total_cost = Column(Float, nullable=False)
    actual_total_cost = Column(Float, nullable=False)
    effected_total_cost = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="SET NULL"), nullable=True)
    order_status_id = Column(Integer, ForeignKey("order_status.id", ondelete="SET NULL"), nullable=True)
    order_bookings = relationship("OrderBookings", backref="order")
    order_custom_data = relationship("OrderCustomData", backref="order")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    def __init__(self, client_name, client_email, phone_number, order_status_id, total_cost, cart_id, actual_total_cost,
                 effected_total_cost, tax_amount,user_id):
        self.client_name = client_name
        self.client_email = client_email
        self.phone_number = phone_number
        self.order_status_id = order_status_id
        self.total_cost = total_cost
        self.cart_id = cart_id
        self.actual_total_cost = actual_total_cost
        self.effected_total_cost = effected_total_cost
        self.tax_amount = tax_amount
        self.user_id = user_id

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

    @classmethod
    def getQuery_OrderByItemSubType(cls, item_subtype_id):
        orders = db.session.query(Order).join(OrderBookings).join(Booking).filter(
            OrderBookings.booking_id == Booking.id).join(
            Item).filter(Item.item_subtype_id == item_subtype_id).group_by(Order)
        return orders
