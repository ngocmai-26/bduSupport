from rest_framework.views import exception_handler
from rest_framework import status

from bduSuport.helpers.response import RestResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if getattr(response.data.get("detail", None), "code", None) in ["authentication_failed", "not_authenticated"]:
        return RestResponse(code="invalid_session", status=status.HTTP_401_UNAUTHORIZED).response

    return response