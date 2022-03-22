from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from model.base import Base, db


class AssociateEmail(Base, db.Model):
    __tablename__ = "associate_email"
    email = Column(String, nullable=False, unique=True)
    status = Column(Boolean, default=True)

    def __init__(self, email, status):
        self.email = email
        self.status = status

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
