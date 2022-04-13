from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from model.base import Base, db


class Logo(Base, db.Model):
    __tablename__ = "logo"
    url = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    def __init__(self, url, user_id):
        self.url = url
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

    @classmethod
    def get_by_user_id(cls, user_id):
        row = cls.query.filter(cls.user_id == user_id).first()
        return row
