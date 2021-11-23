from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class User(Base, db.Model):
    __tablename__ = "user"
    first_name = Column(String, nullable=False, unique=False)
    last_name = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False, unique=True)

    # role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), nullable=False)

    # user_account = relationship("UserAccount", backref="user")

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def insert(self):
        db.session.add(self)
        db.session.commit()
