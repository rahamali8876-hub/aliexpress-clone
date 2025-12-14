from celery import shared_task
from apps.payments.services.stripe_event_service import StripeEventService


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 5})
def process_stripe_event(self, payload: dict):
    StripeEventService().handle(payload)
