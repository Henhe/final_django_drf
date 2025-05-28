from rest_framework.exceptions import APIException
from rest_framework import status


class Exception400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "400. Bad request"
    default_code = "bad_request"


class Exception401(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "401. Not authenticated"
    default_code = "not_authenticated"


class Exception403(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "403. Permission denied"
    default_code = "permission_denied"


class Exception404(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "404. Object not found"
    default_code = "not_found"
