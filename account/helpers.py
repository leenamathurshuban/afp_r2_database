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


from rest_framework_simplejwt.backends import TokenBackend
from account.models import User

def get_user_from_token(request):
    
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
    get_logged_in_user = valid_data['user_id']
    get_user = User.objects.get(id=get_logged_in_user)
    return get_user