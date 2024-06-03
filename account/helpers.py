from rest_framework.response import Response
from rest_framework import status


def get_exception_context(exception=None):
    context = {
        'status':status.HTTP_400_BAD_REQUEST,
        'success':False,
        'response':exception
    }
    return Response(context,status=status.HTTP_400_BAD_REQUEST)

def get_serializer_context(serializer=None):
    context = {
        'status':status.HTTP_200_OK,
        'success':True,
        'response':serializer
    }
    return Response(context,status=status.HTTP_200_OK)