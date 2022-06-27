import paypalrestsdk

from configuration import configs
from model.order import Order

paypalrestsdk.configure({
    "mode": configs.PAYPAL_MODE,
    "client_id": configs.PAYPAL_CLIENT_ID,
    "client_secret": configs.PAYPAL_SECRET_KEY})

domain_url = configs.BASE_API_URL


class PayPal:
    @classmethod
    def create_paypal_session(cls, name, order_id, language, voucher_code, tax_ids):
        order = Order.query_by_id(order_id)
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": domain_url + "checkout_session/success?session_id=notStripe&order_id=" + str(
                    order_id) + "&language=" + str(language) + f"&voucher_code={voucher_code}" + f"&tax_ids={tax_ids}",
                "cancel_url": domain_url + "checkout_session/failed?session_id=notStripe&order_id=" + str(
                    order_id) + "&language=" + str(language) + f"&voucher_code={voucher_code}" + f"&tax_ids={tax_ids}"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": name,
                        "sku": "item",
                        "price": str(order.total_cost),
                        "currency": "EUR",
                        "quantity": 1}]},
                "amount": {
                    "total": str(order.total_cost),
                    "currency": "EUR"},
                "description": f"Order {name} payment."}]})
        if payment.create():
            print("Payment created successfully")
        else:
            print(payment.error)

        approval_url = ""
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                print("Redirect for approval: %s" % (approval_url))
        return approval_url

    @classmethod
    def execute_payment(cls, payment_id, payer_id):
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            print("payment successful.")
        else:
            print("paypal payment failed.")
