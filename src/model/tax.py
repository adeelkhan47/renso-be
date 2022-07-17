from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class Tax(Base, db.Model):
    __tablename__ = "tax"
    name = Column(String, nullable=False)
    percentage = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)
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
