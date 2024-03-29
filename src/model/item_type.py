from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from model.base import Base, db


class ItemType(Base, db.Model):
    __tablename__ = "item_type"
    name = Column(String, nullable=False)
    maintenance = Column(Integer, nullable=False)
    delivery_available = Column(Boolean, nullable=False, unique=False)
    show_time_picker = Column(Boolean, nullable=True, unique=False, default=False)
    DayPickers = relationship("DayPicker", backref="item_type")
    items = relationship("Item", backref="item_type")
    itemTypeTexts = relationship("ItemTypeText", backref="item_type")
    item_sub_type = relationship("ItemSubType", backref="item_type")
    seasonItemTypes = relationship("SeasonItemTypes", backref="item_type")
    itemTypeLocations = relationship("LocationItemTypes", backref="item_type")
    itemTypeExtras = relationship("ItemTypeExtra", backref="item_type")
    itemType_restricted_dates = relationship("RestrictedDates", backref="item_type")
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))

    image = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, name, maintenance, delivery_available, image, user_id, show_time_picker):
        self.name = name
        self.maintenance = maintenance
        self.delivery_available = delivery_available
        self.image = image
        self.user_id = user_id
        self.show_time_picker = show_time_picker

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()

    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def get_by_item_type_name(cls, name, session=None):
        if not session:
            session = db.session
        return session.query(cls).filter(cls.name == name).first()
