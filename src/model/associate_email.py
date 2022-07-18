from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, String, Integer

from model.base import Base, db


class AssociateEmail(Base, db.Model):
    __tablename__ = "associate_email"
    email = Column(String, nullable=False)
    associate_email_subtypes = relationship("AssociateEmailSubtype", backref="associate_email")
    status = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), index=True)
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))

    def __init__(self, email, status, user_id):
        self.email = email
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

    @classmethod
    def update(cls, id, data):
        db.session.query(cls).filter(cls.id == id).update(data)
        db.session.commit()

    @classmethod
    def getall(cls, user_id, session=None):
        if not session:
            session = db.session
        return session.query(cls).filter(cls.user_id == user_id, cls.status == True).all()
