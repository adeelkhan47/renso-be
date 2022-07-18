from sqlalchemy import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class OrderBackUp(Base, db.Model):
    __tablename__ = "order_backup"
    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="SET NULL"), nullable=False)
    unique_key = Column(String, nullable=False)
    paypal_method = Column(String, nullable=False)
    payment_reference = Column(String, nullable=False)
    voucher = Column(String, nullable=True)
    price_paid = Column(String, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))

    def __init__(self, cart_id, unique_key, paypal_method, payment_reference, voucher, price_paid):
        self.cart_id = cart_id
        self.unique_key = unique_key
        self.paypal_method = paypal_method
        self.payment_reference = payment_reference
        self.voucher = voucher
        self.price_paid = price_paid

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
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()

    @classmethod
    def get_order_backUp_by_unique_key(cls, unique_key):
        return cls.query.filter(cls.unique_key == unique_key, cls.is_deleted == False).first()

    @classmethod
    def get_by_cart_id(cls, cart_id, session=None):
        if not session:
            session = db.session
        return session.query(cls).filter(cls.cart_id == cart_id).first()
