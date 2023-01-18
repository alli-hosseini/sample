from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from typing import Callable, List, Dict
from typing import Type


def serialize(serializer: Type[Serializer]) -> Callable:
    def func(f: Callable) -> Callable:
        def wrapper(*args: tuple, **kwargs: Dict):
            request: Request = args[0]
            if request.method.lower() == "post":
                s = serializer(data=request.data)
            else:
                s = serializer(data=request.GET)
            if not s.is_valid():
                if isinstance(s.errors, ReturnDict):
                    res = {
                        "detail": f"{' and '.join(list(s.errors.keys())) } should fill"
                    }
                    return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
                return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)
            return f(*args, **kwargs)

        return wrapper

    return func


def exception_handler(exceptions: List[Type[Exception]]) -> Callable:
    def func(f: Callable) -> Callable:
        def wrapper(*args: tuple, **kwargs: Dict):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if type(e) in exceptions:
                    return Response(
                        data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
                raise e

        return wrapper

    return func
