from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Time

from model.base import Base, db


class TimePicker(Base, db.Model):
    __tablename__ = "time_picker"
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day = Column(String, nullable=False)
    day_picker_id = Column(Integer, ForeignKey("day_picker.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, start_time, end_time, day, day_picker_id):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
        self.day_picker_id = day_picker_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
