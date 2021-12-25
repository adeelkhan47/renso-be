from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class Tag(Base, db.Model):
    __tablename__ = "tag"
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    item_tags = relationship("ItemTag", backref="tag")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
