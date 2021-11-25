from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db


class PaymentMethod(Base, db.Model):
    __tablename__ = "payment_method"
    name = Column(String, nullable=False, unique=False)
    status = Column(Integer, nullable=False, unique=True)

    tax_id = Column(Integer, ForeignKey("tax.id", ondelete="CASCADE"), nullable=True)

    def __init__(self, name, status, tax_id):
        self.name = name
        self.status = status
        self.tax_id = tax_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
