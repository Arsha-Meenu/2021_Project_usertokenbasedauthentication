from django.shortcuts import render
from django.http import HttpResponse, Http404



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer,UserLoginSerializer
from django.contrib.auth import authenticate

from user_auth_app.models import Library
from django.contrib.auth import get_user_model

from rest_framework import permissions

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated


User = get_user_model()



class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny]}

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def list(self,pk, request, *args, **kwargs):
        userData = User.objects.get(pk)

        return super(UserViewSet, self).list(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A viewset that provides the standard actions
#     """
#     queryset = User.objects.all()
#     serializer_class = UserLoginSerializer

#     @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])
#     def set_password(self, request, pk=None):
#         user = self.get_object()
#         serializer = PasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user.set_password(serializer.data['password'])
#             user.save()
#             return Response({'status': 'password set'})
#         else:
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)

    















# Create simpleapi function
class simpleapi(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,format = None):
        return Response({'text':'hai,welcome to DjangoRestFramework.'},status=status.HTTP_200_OK)

#create  a class for user registration
class registerClass(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,format = None):
        serializer = RegisterSerializer(data =request.data) 
        data = {}#create a null dictionary to return the data
        if serializer.is_valid():
            serializedData = serializer.save()
            data['id'] = serializedData.id
            data["Response"]='Registered'
            data['username'] = serializedData.username
            data['email'] = serializedData.email
        else:
            data = serializer.errors # return error if serializer is not valid
        return Response(data)

# create a class for user login
class loginClass(APIView):
    permission_classes = (AllowAny,)

    def post(self,request,format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error':'Please provide username and password'},status=status.HTTP_400_BAD_REQUEST)
        userData = authenticate(username = username, password= password)
        if not userData :
            return Response({'error':'Invalid Credentials'},status=status.HTTP_404_NOT_FOUND)
        token,_ = Token.objects.get_or_create (user = userData) #create token for user
        return Response({'id':userData.id,'username':userData.username,'token':token.key},status=status.HTTP_200_OK)


# fetch ,create and delete the details by a particular user(Will identify the user using the token)
class getDetailsClass(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny]}
    
    def get_object(self,pk):
        try:
            return User.objects.get(pk = pk)
        except:
            raise Http404
            # return Response(status = status.HTTP_404_NOT_FOUND)



    def list(self,request,pk,format =None):
        userData = self.get_object(pk)
        # user = request.user.id
        # if userData.id != user:
        #     return Response({'response':'you dont have permission to read single object data.'})
        serializer =UserLoginSerializer(userData,many =True)
        # return Response(serializer.data)
        return super(getDetailsClass, self).list(request)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


    def put(self, request,pk,  format=None):        
        modify = self.get_object(pk)
        # user = request.user.id
        # if modify.id != user:
        #     return Response({'response':'you dont have permission to edit that.'})
        serializer = UserLoginSerializer(modify, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):        
        deletedata = self.get_object(pk)
        user = request.user.id
        if deletedata.id != user:
            return Response({'response':'you dont have permission to delete that.'})
        deletedata.delete()
        return Response('successfully deleted the single object',status=status.HTTP_200_OK)

        
