from rest_framework import status
from rest_framework.exceptions import APIException


class PaymentNotAvailable(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Payment does not exist"


class PaymentCanceled(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Payment is canceled"


class PaymentIsNotSucceeded(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Payment is not succeeded"


class PaymentNotSaved(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Payment method not saved"


class PaymentDisable(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Payment method has been disabled so we removed it from your account"


class RefundDisable(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Refund is not available"
