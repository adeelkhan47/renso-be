from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, String, Integer

from model.base import Base, db


class PaymentMethod(Base, db.Model):
    __tablename__ = "payment_method"
    name = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    payment_tax = relationship("PaymentTax", backref="payment_method")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    def __init__(self, name, status, user_id):
        self.name = name
        self.status = status
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
    def get_payment_method_by_name(cls, name, user_id):
        return cls.query.filter(cls.name == name, cls.status == True, cls.user_id == user_id).first()
