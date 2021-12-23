from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Boolean

from model.base import Base, db


class User(Base, db.Model):
    __tablename__ = "user"
    name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    subscription = Column(String, nullable=True)
    status = Column(Boolean, nullable=True)

    items = relationship("Item", backref="user")

    def __init__(self, name, email, password, subscription, status):
        self.name = name
        self.password = password
        self.email = email
        self.subscription = subscription
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def update(cls, user_id, updated_user_data):
        db.session.query(cls).filter(cls.id == user_id).update(updated_user_data)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
