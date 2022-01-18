from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Boolean

from model.base import Base, db


class PaymentMethod(Base, db.Model):
    __tablename__ = "payment_method"
    name = Column(String, nullable=False, unique=True)
    status = Column(Boolean, nullable=False)
    payment_tax = relationship("PaymentTax", backref="payment_method")

    def __init__(self, name, status):
        self.name = name
        self.status = status

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
