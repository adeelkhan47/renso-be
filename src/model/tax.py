from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class Tax(Base, db.Model):
    __tablename__ = "tax"
    name = Column(String, nullable=False)
    percentage = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    payment_tax = relationship("PaymentTax", backref="tax")
    itemSubTypeTaxs = relationship("ItemSubTypeTaxs", backref="tax")

    def __init__(self, name, percentage, description, user_id):
        self.name = name
        self.percentage = percentage
        self.description = description
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
