from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db
from model.item_status import ItemStatus


class Item(Base, db.Model):
    __tablename__ = "item"
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    status_id = Column(Integer, ForeignKey("item_status.id", ondelete="CASCADE"), nullable=True)
    person = Column(Integer, nullable=False)

    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="CASCADE"), nullable=True)
    bookings = relationship("Booking", backref="item")
    item_tags = relationship("ItemTag", backref="item")

    def __init__(self, name, image, description, price, status_id, person, item_type_id):
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.status_id = status_id
        self.person = person
        self.item_type_id = item_type_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()

    @classmethod
    def get_all_active_items(cls):
        item_status_id = ItemStatus.get_id_by_name("Available")
        return db.session.query(cls).filter(cls.status_id == item_status_id).all()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def get_all_active_items_by_item_type_id(cls, item_type_id):
        item_status_id = ItemStatus.get_id_by_name("Available")
        return db.session.query(cls).filter(cls.item_type_id == item_type_id, cls.status_id == item_status_id).all()
