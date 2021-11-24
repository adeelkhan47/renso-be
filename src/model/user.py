from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class User(Base, db.Model):
    __tablename__ = "user"
    name = Column(String, nullable=True, unique=False, )
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True, unique=False)
    subscription = Column(String, nullable=True, unique=True)
    status = Column(String, nullable=True, unique=True)

    # role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), nullable=False)

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
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
