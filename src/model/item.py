from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.item_tag import ItemTag
from model.item_location import ItemLocation
from model.base import Base, db
from model.item_status import ItemStatus


class Item(Base, db.Model):
    __tablename__ = "item"
    name = Column(String, nullable=False)
    image = Column(String(500), nullable=False)
    description = Column(String, nullable=False)

    item_status_id = Column(Integer, ForeignKey("item_status.id", ondelete="SET NULL"), nullable=True)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="SET NULL"), nullable=False)
    item_subtype_id = Column(Integer, ForeignKey("item_subtype.id", ondelete="SET NULL"), nullable=False)
    bookings = relationship("Booking", backref="item")
    item_tags = relationship("ItemTag", backref="item")
    item_locations = relationship("ItemLocation", backref="item")
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, name, image, description, item_status_id, item_type_id, item_subtype_id, user_id):
        self.name = name
        self.image = image
        self.description = description
        self.item_status_id = item_status_id
        self.item_type_id = item_type_id
        self.item_subtype_id = item_subtype_id
        self.user_id = user_id

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
    def get_all_active_items(cls, user_id):
        item_status_id = ItemStatus.get_id_by_name("Available")
        return db.session.query(cls).filter(cls.item_status_id == item_status_id, cls.user_id == user_id).all()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def get_all_active_items_by_item_type_id(cls, item_type_id):
        item_status_id = ItemStatus.get_id_by_name("Available")
        return db.session.query(cls).filter(cls.item_type_id == item_type_id,
                                            cls.item_status_id == item_status_id).all()
