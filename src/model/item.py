from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db


class Item(Base, db.Model):
    __tablename__ = "item"
    name = Column(String, nullable=False, unique=False)
    image = Column(String, nullable=False, unique=True)
    tags = Column(String, nullable=False, unique=False)
    description = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False, unique=True)

    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, name, image, tags, description, price, user_id):
        self.name = name
        self.image = image
        self.tags = tags
        self.description = description
        self.price = price
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
