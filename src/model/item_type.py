from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Integer, Boolean

from model.base import Base, db


class ItemType(Base, db.Model):
    __tablename__ = "item_type"
    name = Column(String, nullable=False, unique=True)
    maintenance = Column(Integer, nullable=False)
    delivery_available = Column(Boolean, nullable=False, unique=False)
    DayPickers = relationship("DayPicker", backref="item_type")
    items = relationship("Item", backref="item_type")
    item_sub_type = relationship("ItemSubType", backref="item_type")
    seasonItemTypes = relationship("SeasonItemTypes", backref="item_type")

    def __init__(self, name, maintenance, delivery_available):
        self.name = name
        self.maintenance = maintenance
        self.delivery_available = delivery_available

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
