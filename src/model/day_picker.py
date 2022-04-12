from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer

from model.base import Base, db


class DayPicker(Base, db.Model):
    __tablename__ = "day_picker"
    monday = Column(Boolean, nullable=False)
    tuesday = Column(Boolean, nullable=False)
    wednesday = Column(Boolean, nullable=False)
    thursday = Column(Boolean, nullable=False)
    friday = Column(Boolean, nullable=False)
    saturday = Column(Boolean, nullable=False)
    sunday = Column(Boolean, nullable=False)
    item_type_id = Column(Integer, ForeignKey("item_type.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, monday, tuesday, wednesday, thursday, friday, saturday, sunday, item_type_id):
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.item_type_id = item_type_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
    @classmethod
    def update(cls, day_picker_id, day_picker_data):
        db.session.query(cls).filter(cls.id == day_picker_id).update(day_picker_data)
        db.session.commit()
