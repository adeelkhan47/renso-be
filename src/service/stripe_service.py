import logging

import stripe
from stripe.error import (
    APIConnectionError,
    AuthenticationError,
    InvalidRequestError,
    RateLimitError,
    SignatureVerificationError,
    StripeError,
)
from stripe.http_client import RequestsClient

stripe_keys = {
    "secret_key": "secret_key",
    "publishable_key": "publishable_key",
}
stripe.api_key = stripe_keys["secret_key"]
stripe.default_http_client = RequestsClient()


class Stripe:
    @classmethod
    def create_checkout_session(cls, price_key):
        """
        create checkout session for given price

        :param price_key:
        :return:
        """
        domain_url = "http://127.0.0.1:5001/"
        stripe.api_key = stripe_keys["secret_key"]
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url
                            + "checkout_session/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url
                           + "checkout_session/failed?session_id={CHECKOUT_SESSION_ID}",
                payment_method_types=["card"],
                mode="payment",
                line_items=[{"quantity": 1, "price": price_key}],
            )
            return checkout_session["id"]

        except (
                RateLimitError,
                InvalidRequestError,
                AuthenticationError,
                APIConnectionError,
                StripeError,
                SignatureVerificationError,
        ) as e:
            logging.exception(e)
            return None

    @classmethod
    def expire_session(cls, session_id):
        try:
            stripe.checkout.Session.expire(session_id)
            return True
        except (
                RateLimitError,
                InvalidRequestError,
                AuthenticationError,
                APIConnectionError,
                StripeError,
                SignatureVerificationError,
        ) as e:
            logging.exception(e)
            return None

    @classmethod
    def retrieve_session(cls, session_id):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return session
        except (
                RateLimitError,
                InvalidRequestError,
                AuthenticationError,
                APIConnectionError,
                StripeError,
                SignatureVerificationError,
        ) as e:
            logging.exception(e)
            return None

    @classmethod
    def create_product(cls, name):
        try:
            product = stripe.Product.create(name=name)

            return product["id"]
        except (
                RateLimitError,
                InvalidRequestError,
                AuthenticationError,
                APIConnectionError,
                StripeError,
                SignatureVerificationError,
        ) as e:
            logging.exception(e)
            return None

    @classmethod
    def create_price(cls, product_id, price):
        try:
            price = stripe.Price.create(
                unit_amount=int(price*100),
                currency="eur",
                product=product_id
            )
            return price["id"]
        except (
                RateLimitError,
                InvalidRequestError,
                AuthenticationError,
                APIConnectionError,
                StripeError,
                SignatureVerificationError,
        ) as e:
            logging.exception(e)
            return None
