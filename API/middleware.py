from http import HTTPStatus

from django.http import JsonResponse


class JSONErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.status_code_description = {
            v.value: v.description for v in HTTPStatus
        }

    def __call__(self, request):
        response = self.get_response(request)

        if not request.content_type == 'application/json':
            return response

        status_code = response.status_code
        if (
            not HTTPStatus.BAD_REQUEST
            < status_code
            <= HTTPStatus.INTERNAL_SERVER_ERROR
        ):
            return response

        r = JsonResponse(
            {
                "error": {
                    "status_code": status_code,
                    "message": self.status_code_description[status_code],
                    "detail": {"url": request.get_full_path()}
                }
            }
        )
        r.status_code = status_code
        return r
