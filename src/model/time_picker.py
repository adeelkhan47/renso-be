from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Time
from sqlalchemy import text
from model.base import Base, db


class TimePicker(Base, db.Model):
    __tablename__ = "time_picker"
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day = Column(String, nullable=False)

    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)
    day_picker_id = Column(Integer, ForeignKey("day_picker.id", ondelete="SET NULL"), nullable=False)

    def __init__(self, start_time, end_time, day, day_picker_id, user_id):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
        self.day_picker_id = day_picker_id
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()
