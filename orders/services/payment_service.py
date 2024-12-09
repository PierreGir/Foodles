import requests
from requests.exceptions import RequestException


class PaymentService:
    @staticmethod
    def process_payment(amount, customer_id):
        """
        Call payment API
        """
        try:
            # return {"success": True}
            response = requests.post(
                "https://external-provider.com/api/refund/",
                json={"amount": float(amount), "client_id": customer_id},
                timeout=5,
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"success": False, "error": str(e)}
