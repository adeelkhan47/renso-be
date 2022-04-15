from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from model.base import Base, db


class Tag(Base, db.Model):
    __tablename__ = "tag"
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    color = Column(String, nullable=True)
    item_tags = relationship("ItemTag", backref="tag")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    def __init__(self, name, description, color, user_id):
        self.name = name
        self.description = description
        self.color = color
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
