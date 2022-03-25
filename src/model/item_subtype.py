from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from model.base import Base, db


class ItemSubType(Base, db.Model):
    __tablename__ = "item_subtype"
    name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False, unique=False)
    person = Column(Integer, nullable=False, unique=False)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="CASCADE"), nullable=True)
    items = relationship("Item", backref="item_subtype")
    associate_email_subtypes = relationship("AssociateEmailSubtype", backref="item_subtype")
    dayPicker = relationship("DayPicker", backref="item_subtype")

    def __init__(self, name, price, person, item_type_id):
        self.name = name
        self.price = price
        self.person = person
        self.item_type_id = item_type_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def get_by_item_type_id(cls, item_type_id):
        rows = cls.query.filter(cls.item_type_id == item_type_id).all()
        return rows
