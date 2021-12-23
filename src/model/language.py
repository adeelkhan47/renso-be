from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class Language(Base, db.Model):
    __tablename__ = "language"
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
