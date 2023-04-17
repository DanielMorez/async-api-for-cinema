from rest_framework import status
from rest_framework.exceptions import APIException


class ActiveSubscriptionExists(APIException):
    default_detail = "User has active subscription"
    status_code = status.HTTP_400_BAD_REQUEST


class PaymentNotAvailable(APIException):
    default_detail = "Payment is not available"
    status_code = status.HTTP_400_BAD_REQUEST
