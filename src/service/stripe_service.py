import logging

import stripe
from stripe.error import (APIConnectionError, AuthenticationError,
                          InvalidRequestError, RateLimitError,
                          SignatureVerificationError, StripeError)
from stripe.http_client import RequestsClient

from configuration import configs

stripe_keys = {
    "secret_key": configs.STRIPE_SECRET_KEY,
    "publishable_key": configs.STRIPE_PUBLIC_KEY,
}
stripe.api_key = stripe_keys["secret_key"]
stripe.default_http_client = RequestsClient()


class Stripe:
    @classmethod
    def create_checkout_session(cls, price_key, order_id, language, voucher_code):
        """
        create checkout session for given price

        :param voucher_code:
        :param order_id:
        :param language:
        :param price_key:
        :return:
        """
        domain_url = configs.BASE_API_URL
        stripe.api_key = stripe_keys["secret_key"]
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "checkout_session/success?session_id={CHECKOUT_SESSION_ID}&order_id=" + str(
                    order_id) + "&language=" + str(language) + f"&voucher_code={voucher_code}",
                cancel_url=domain_url + "checkout_session/failed?session_id={CHECKOUT_SESSION_ID}&order_id=" + str(
                    order_id) + "&language=" + str(language) + f"&voucher_code={voucher_code}",
                payment_method_types=["card", "klarna", "eps", "ideal", "alipay", "bancontact", "p24", "sepa_debit",
                                      "sofort", "giropay"],
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
                unit_amount=int(price * 100),
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
