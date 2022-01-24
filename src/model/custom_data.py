from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from model.base import Base, db


class CustomData(Base, db.Model):
    __tablename__ = "custom_data"
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    order_custom_data = relationship("OrderCustomData", backref="custom_data")

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
