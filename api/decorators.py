from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def permission_required(func):
    @wraps(func)
    def inner(self, request, *args, **kwargs):
        # Check permissions for non-GET requests
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Allow only superusers to perform write actions
            if not request.user.is_superuser:
                return Response(
                    {'detail': 'Only superusers can perform this action.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Check permissions for GET requests
        elif request.method == "GET":
            # Allow only authenticated users to view content
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication is required to view this content.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        return func(self, request, *args, **kwargs)

    return inner
