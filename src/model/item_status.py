from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class ItemStatus(Base, db.Model):
    __tablename__ = "item_status"
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    item_status = relationship("Item", backref="item_status")

    def __init__(self, name, color):
        self.name = name
        self.color = color

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
    def get_id_by_name(cls, name: str):
        row = db.session.query(cls).filter_by(name=name).first()
        return row.id
