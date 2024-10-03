from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def permission_required(func):
    @wraps(func)
    def inner(self, request, *args, **kwargs):
        # Check permissions based on the request method
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Check if user is superuser
            if not request.user.is_superuser:
                return Response(
                    {'detail': 'You do not have permission to perform this action.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.method in ["GET"]:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'You must be logged in to perform this action.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        return func(self, request, *args, **kwargs)

    return inner
