import requests


CUR_EGYPT =  '£'
CUR_QATAR = CUR_OMAN = CUR_SAUDI_ARABIA = '﷼'
CUR_BAHRAIN = 'BD'
CUR_UNITED_ARAB_EMIRATES = 'د.إ'
CUR_JORDAN = 'Dinar'
CUR_KUWAIT = 'ك'
CUR_INTERNATIONAL = '$'

CURRENCIES = {
    'Egypt': CUR_EGYPT,
    'Qatar': CUR_QATAR,
    'Bahrain': CUR_BAHRAIN,
    'Saudi Arabia': CUR_SAUDI_ARABIA,
    'United Arab Emirates': CUR_UNITED_ARAB_EMIRATES,
    'Jordan': CUR_JORDAN,
    'Kuwait': CUR_KUWAIT,
    'Oman': CUR_OMAN,
    'International': CUR_INTERNATIONAL,
}


class URLs:
    def __init__(self):
        self.base_url = "https://accept.paymob.com/api/"

        # auth
        self.auth = "auth/tokens"

        # ecommerce
        self.order = "ecommerce/orders"
        self.inquire_transaction = "ecommerce/orders/transaction_inquiry"
        self.tracking = "ecommerce/orders/{order_id}/delivery_status?token={token}".format(order_id="{order_id}",
                                                                                           token="{token}")
        self.preparing_package = "ecommerce/orders/{order_id}/airway_bill?token={token}".format(order_id="{order_id}",
                                                                                                token="{token}")

        # acceptance
        self.payment_key = "acceptance/payment_keys"
        self.payment = "acceptance/payments/pay"
        self.capture = "acceptance/capture"
        self.refund = "acceptance/void_refund/refund"
        self.void = "acceptance/void_refund/void?token={token}".format(token="{token}")
        self.retrieve_transaction = "acceptance/transactions/{id}?token={token}".format(id="{id}", token="{token}")
        self.loyalty_checkout = "acceptance/loyalty_checkout"
        self.iframe = "acceptance/iframes/{iframe_id}?payment_token={payment_token}".format(iframe_id="{iframe_id}",
                                                                                            payment_token="{payment_token}")

    def base_url(self):
        return self.base_url

    def authentication_url(self):
        return self.base_url + self.auth

    def order_registration_url(self):
        return self.base_url + self.order

    def payment_key_url(self):
        return self.base_url + self.payment_key

    def payment_url(self):
        return self.base_url + self.payment

    def capture_transaction_url(self):
        return self.base_url + self.capture

    def refund_transaction_url(self):
        return self.base_url + self.refund

    def void_transaction_url(self):
        return self.base_url + self.void

    def retrieve_transaction_url(self):
        return self.base_url + self.retrieve_transaction

    def inquire_transaction_with_order_details_url(self):
        return self.base_url + self.inquire_transaction

    def tracking_url(self):
        return self.base_url + self.tracking

    def preparing_package_url(self):
        return self.base_url + self.preparing_package

    def loyalty_checkout_url(self):
        return self.base_url + self.loyalty_checkout

    def iframe_url(self):
        return self.base_url + self.iframe


class AcceptAPI:
    def __init__(self, API_KEY):
        self.api_key = API_KEY
        self.url = URLs()

    def retrieve_auth_token(self):
        """
        Authentication Request:
        :return: token: Authentication token, which is valid for one hour from the creation time.
        """
        data = {'api_key': self.api_key}
        r = requests.post(self.url.authentication_url(), json=data)
        token = r.json().get('token')
        return token

    def order_registration(self, data):
        """
        Order Registration API
        :param data: Order data
        :return: registered order
        """
        r = requests.post(self.url.order_registration_url(), json=data)
        order = r.json()
        return order

    def payment_key_request(self, data):
        r = requests.post(self.url.payment_key_url(), json=data)
        payment_token = r.json().get('token')
        return payment_token

    def pay(self, identifier, payment_method, payment_token):
        data = {
            "source": {
                "identifier": identifier,
                "subtype": payment_method
            },
            "payment_token": payment_token
        }
        r = requests.post(self.url.payment_url(), json=data)
        transaction = r.json()
        return transaction

    def capture_transaction(self, transaction_id, amount_cents):
        auth_token = self.retrieve_auth_token()
        data = {
            "auth_token": auth_token,
            "transaction_id": transaction_id,
            "amount_cents": amount_cents
        }
        r = requests.post(self.url.capture_transaction_url(), json=data)

        transaction = r.json()
        return transaction

    def refund_transaction(self, transaction_id, amount_cents):
        auth_token = self.retrieve_auth_token()
        data = {
            "auth_token": auth_token,
            "transaction_id": transaction_id,
            "amount_cents": amount_cents
        }
        r = requests.post(self.url.refund_transaction_url(), json=data)

        transaction = r.json()
        return transaction

    def void_transaction(self, transaction_id):
        auth_token = self.retrieve_auth_token()
        data = {
            "transaction_id": transaction_id,
        }
        r = requests.post(self.url.void_transaction_url().format(token=str(auth_token)), json=data)

        transaction = r.json()
        return transaction

    def retrieve_transaction(self, transaction_id):
        auth_token = self.retrieve_auth_token()
        r = requests.get(self.url.retrieve_transaction_url().format(id=str(transaction_id),
                                                                    token=str(auth_token)))
        transaction = r.json()
        return transaction

    def inquire_transaction(self, merchant_order_id, order_id):
        auth_token = self.retrieve_auth_token()
        payload = {
            "auth_token": auth_token,
            "merchant_order_id": merchant_order_id,
            "order_id": order_id
        }

        r = requests.post(self.url.inquire_transaction_with_order_details_url(), json=payload)

        transaction = r.json()
        return transaction

    def tracking(self, order_id):
        auth_token = self.retrieve_auth_token()
        r = requests.get(self.url.tracking_url().format(order_id=str(order_id),
                                                        token=str(auth_token)))
        order = r.json()
        return order

    def preparing_package(self, order_id):
        auth_token = self.retrieve_auth_token()
        pdf_link = self.url.preparing_package_url().format(order_id=str(order_id), token=str(auth_token))
        return pdf_link

    def loyalty_checkout(self, transaction_reference, otp, payment_token):
        data = {
            "reference": transaction_reference,
            "otp": otp,
            "payment_token": payment_token
        }

        r = requests.post(self.url.loyalty_checkout_url(), json=data)
        response = r.json()
        return response

    def retrieve_iframe(self, iframe_id, payment_token):
        return self.url.iframe_url().format(iframe_id=iframe_id, payment_token=payment_token)
