from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class DatePicker(Base, db.Model):
    __tablename__ = "date_picker"
    allowed_days = Column(String, nullable=False, unique=False)
    not_allowed_days = Column(String, nullable=False, unique=True)

    def __init__(self, allowed_days, not_allowed_days):
        self.allowed_days = allowed_days
        self.not_allowed_days = not_allowed_days

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
