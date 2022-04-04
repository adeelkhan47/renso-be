from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db
from model.item_status import ItemStatus


class Item(Base, db.Model):
    __tablename__ = "item"
    name = Column(String, nullable=False)
    image = Column(String(500), nullable=False)
    image_key = Column(String, nullable=False)
    description = Column(String, nullable=False)

    item_status_id = Column(Integer, ForeignKey("item_status.id", ondelete="SET NULL"), nullable=True)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="CASCADE"), nullable=False)
    item_subtype_id = Column(Integer, ForeignKey("item_subtype.id", ondelete="CASCADE"), nullable=False)
    bookings = relationship("Booking", backref="item")
    item_tags = relationship("ItemTag", backref="item")
    item_locations = relationship("ItemLocation", backref="item")

    def __init__(self, name, image, description, item_status_id, item_type_id, item_subtype_id, image_key):
        self.name = name
        self.image = image
        self.image_key = image_key
        self.description = description
        self.item_status_id = item_status_id
        self.item_type_id = item_type_id
        self.item_subtype_id = item_subtype_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()

    @classmethod
    def get_all_active_items(cls):
        item_status_id = ItemStatus.get_id_by_name("Available")
        return db.session.query(cls).filter(cls.item_status_id == item_status_id).all()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def get_all_active_items_by_item_type_id(cls, item_type_id):
        item_status_id = ItemStatus.get_id_by_name("Available")
        return db.session.query(cls).filter(cls.item_type_id == item_type_id,
                                            cls.item_status_id == item_status_id).all()
