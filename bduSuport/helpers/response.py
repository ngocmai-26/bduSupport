from rest_framework.response import Response

class RestResponse():
    content_type = "application/json"

    def __init__(self, data: dict = None, code: str = "success", message: str = "", status: int = 200) -> None:
        self.__data = data
        self.__message = message
        self.__code = code
        self.__status = status
    
    @property
    def response(self):
        return Response(
            {
                "data": self.__data,
                "code": self.__code,
                "message": self.__message,
            },
            status=self.__status,
            content_type=self.content_type
        )