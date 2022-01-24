from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from model.base import Base, db


class OrderCustomData(Base, db.Model):
    __tablename__ = "order_custom_data"

    custom_data_id = Column(Integer, ForeignKey("custom_data.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, custom_data_id, order_id):
        self.custom_data_id = custom_data_id
        self.order_id = order_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def delete_by_order_id(cls, order_id):
        cls.query.filter(cls.order_id == order_id).delete()
        db.session.commit()
