from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db


class Tag(Base, db.Model):
    __tablename__ = "tag"
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    color = Column(String, nullable=True)
    item_tags = relationship("ItemTag", backref="tag")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))

    def __init__(self, name, description, color, user_id):
        self.name = name
        self.description = description
        self.color = color
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
