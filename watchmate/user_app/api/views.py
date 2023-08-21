from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import UserRegistrationSerializer
# from rest_framework.authoken.models import Token 
@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            
            # data['response'] = Re
            data['username'] = account.username 
            data['email'] = account.email 

            token = Token.objects.get(user = account).key 
            data['token'] = token     
            # return Response(serializer.data)
            
        else: 
            data = serializer.errors
        return Response(data)