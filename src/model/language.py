from sqlalchemy import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, String, Integer

from model.base import Base, db


class Language(Base, db.Model):
    __tablename__ = "language"
    name = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, name, status, user_id):
        self.name = name
        self.status = status
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
