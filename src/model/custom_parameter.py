from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Boolean

from model.base import Base, db


class CustomParameter(Base, db.Model):
    __tablename__ = "custom_parameter"
    name = Column(String, nullable=False)
    mandatory = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    def __init__(self, name, mandatory, user_id):
        self.name = name
        self.mandatory = mandatory
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()
