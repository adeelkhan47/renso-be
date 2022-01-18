from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db


class Tax(Base, db.Model):
    __tablename__ = "tax"
    name = Column(String, nullable=False, unique=True)
    percentage = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

    payment_tax = relationship("PaymentTax", backref="tax")

    def __init__(self, name, percentage, description):
        self.name = name
        self.percentage = percentage
        self.description = description

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
