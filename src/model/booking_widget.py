from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, String, Integer

from model.base import Base, db


class BookingWidget(Base, db.Model):
    __tablename__ = "booking_widget"
    __table_args__ = {'extend_existing': True}
    day_picker_status = Column(Boolean, default=True)
    time_picker_status = Column(Boolean, default=True)
    date_range_picker_status = Column(Boolean, default=True)
    apply_vouchers_status = Column(Boolean, default=True)
    apply_months_factor_status = Column(Boolean, default=True)
    apply_location_factor_status = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, day_picker_status, time_picker_status, date_range_picker_status, apply_vouchers_status,
                 apply_months_factor_status, apply_location_factor_status, user_id):
        self.day_picker_status = day_picker_status
        self.time_picker_status = time_picker_status
        self.date_range_picker_status = date_range_picker_status
        self.apply_vouchers_status = apply_vouchers_status
        self.apply_months_factor_status = apply_months_factor_status
        self.apply_location_factor_status = apply_location_factor_status
        self.user_id = user_id



    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

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
