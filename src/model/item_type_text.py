from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import text as _text
from model.base import Base, db


class ItemTypeText(Base, db.Model):
    __tablename__ = "item_type_text"
    text = Column(String(300), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=_text("False"))
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="SET NULL"), nullable=False, index=True,
                          unique=True)

    def __init__(self, text, item_type_id):
        self.text = text
        self.item_type_id = item_type_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()


    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()

    @classmethod
    def get_by_item_type_id(cls, item_type_id):
        return cls.query.filter(cls.item_type_id == item_type_id).first()
