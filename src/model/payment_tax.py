from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class PaymentTax(Base, db.Model):
    __tablename__ = "payment_tax"

    tax_id = Column(Integer, ForeignKey("tax.id", ondelete="CASCADE"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payment_method.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, tax_id, payment_id):
        self.tax_id = tax_id
        self.payment_id = payment_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_payment_id(cls, payment_id):
        cls.query.filter(cls.payment_id == payment_id).delete()
        db.session.commit()
