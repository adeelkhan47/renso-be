from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, Boolean

from model.base import Base, db


class ItemSubType(Base, db.Model):
    __tablename__ = "item_subtype"
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    show_description = Column(Boolean, nullable=True)
    price = Column(Float, nullable=False, unique=False)
    person = Column(Integer, nullable=False, unique=False)
    image = Column(String(500), nullable=False)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="SET NULL"), nullable=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="SET NULL"), nullable=True)
    least_price = Column(Float, nullable=True, unique=False, default=1)
    discount_after_higher_price = Column(Integer, nullable=True, unique=False, default=10)
    same_price_days = Column(Integer, nullable=True, unique=False, default=1)

    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    items = relationship("Item", backref="item_subtype")
    associate_email_subtypes = relationship("AssociateEmailSubtype", backref="item_subtype")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)
    itemTypeExtras = relationship("ItemTypeExtra", backref="item_subtype")
    itemSubTypeTaxs = relationship("ItemSubTypeTaxs", backref="item_subtype")

    def __init__(self, name, price, person, item_type_id, image, user_id, least_price, discount_after_higher_price,
                 same_price_days, show_description, description, company_id):
        self.name = name
        self.price = price
        self.person = person
        self.item_type_id = item_type_id
        self.image = image
        self.user_id = user_id
        self.least_price = least_price
        self.discount_after_higher_price = discount_after_higher_price
        self.same_price_days = same_price_days
        self.show_description = show_description
        self.description = description
        self.company_id = company_id

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
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def soft_delete_on_item_type(cls, item_type_id):
        db.session.query(cls).filter(cls.item_type_id == item_type_id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def get_by_item_type_id(cls, item_type_id):
        rows = cls.query.filter(cls.item_type_id == item_type_id, cls.is_deleted == False).all()
        return rows
