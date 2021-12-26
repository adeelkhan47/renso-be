from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class ItemTag(Base, db.Model):
    __tablename__ = "item_tag"

    tag_id = Column(Integer, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, tag_id, item_id):
        self.tag_id = tag_id
        self.item_id = item_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_item_id(cls, item_id):
        cls.query.filter(cls.item_id == item_id).delete()
        db.session.commit()
