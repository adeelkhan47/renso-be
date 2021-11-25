from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class Order(Base, db.Model):
    __tablename__ = "order"
    client_name = Column(String, nullable=False, unique=False)
    client_email = Column(String, nullable=False, unique=False)
    phone_number = Column(String, nullable=False, unique=False)
    status = Column(String, nullable=False, unique=False)
    time_period = Column(String, nullable=False, unique=False)

    order_bookings = relationship("OrderBookings", backref="order")

    def __init__(self, client_name, client_email, phone_number, status, time_period):
        self.client_name = client_name
        self.client_email = client_email
        self.phone_number = phone_number
        self.status = status
        self.time_period = time_period

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
