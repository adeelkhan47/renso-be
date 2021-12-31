from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Float

from model.base import Base, db


class Order(Base, db.Model):
    __tablename__ = "order"
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    status = Column(String, nullable=False)
    time_period = Column(String, nullable=False)
    total_cost = Column(Float, nullable=False)

    order_bookings = relationship("OrderBookings", backref="order")

    def __init__(self, client_name, client_email, phone_number, status, time_period, total_cost):
        self.client_name = client_name
        self.client_email = client_email
        self.phone_number = phone_number
        self.status = status
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
