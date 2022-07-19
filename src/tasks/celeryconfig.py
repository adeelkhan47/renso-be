from celery.schedules import crontab

from configuration import configs

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

broker_url = configs.CELERY_BROKER_REDIS
broker_transport_options = {"visibility_timeout": 3600 * 6}
result_backend = configs.CELERY_BROKER_REDIS
result_persistent = False

imports = "tasks.order"

beat_schedule = {
    "remove_pending_every_10_min": {
        "task": "tasks.order.remove_pending",
        "schedule": crontab(minute="*/10"),
    }, "mark_order_complete_if_payment_pending_every_hour_at_3rd_min": {
        "task": "tasks.order.mark_order_complete_if_payment_pending",
        "schedule": crontab(minute="3", hour="*"),
    }, "mark_order_complete_if_bookings_completed_every_hour_at_12th_min": {
        "task": "tasks.order.mark_order_complete_on_completion",
        "schedule": crontab(minute="*/2"),
    },
}
