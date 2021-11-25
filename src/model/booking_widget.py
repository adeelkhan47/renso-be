from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class BookingWidget(Base, db.Model):
    __tablename__ = "booking_widget"
    name = Column(String, nullable=False, unique=False)
    status = Column(String, nullable=False, unique=True)

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
