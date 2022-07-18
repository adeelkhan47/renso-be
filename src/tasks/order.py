import logging

from model.booking import Booking
from model.order import Order
from tasks.celery import DbTask, celery_app

logger = logging.getLogger(__file__)


@celery_app.task(bind=True, base=DbTask)
def remove_pending(self, *args, **kwargs):
    session = self.session
    Booking.delete_pending_bookings(session)


@celery_app.task(bind=True, base=DbTask)
def mark_order_complete_if_payment_pending(self, *args, **kwargs):
    session = self.session
    Order.get_pending_order_and_mark_complete(session)

@celery_app.task(bind=True, base=DbTask)
def mark_order_complete_on_completion(self, *args, **kwargs):
    session = self.session
    Order.get_completed_order_and_mark_complete(session)

