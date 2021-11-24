from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db


class ItemType(Base, db.Model):
    __tablename__ = "item_type"
    name = Column(String, nullable=False, unique=False)
    maintenance = Column(Integer, nullable=False, unique=True)
    delivery_available = Column(String, nullable=False, unique=False)

    items = relationship("Item", backref="item_type")

    def __init__(self, name, maintenance, delivery_available):
        self.name = name
        self.maintenance = maintenance
        self.delivery_available = delivery_available

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
