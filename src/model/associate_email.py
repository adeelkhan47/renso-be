from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, String, Integer

from model.base import Base, db


class AssociateEmail(Base, db.Model):
    __tablename__ = "associate_email"
    email = Column(String, nullable=False, unique=True)
    associate_email_subtypes = relationship("AssociateEmailSubtype", backref="associate_email")
    status = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True)

    def __init__(self, email, status, user_id):
        self.email = email
        self.status = status
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
