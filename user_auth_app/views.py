from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets,views
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer,UserLoginSerializer,UserViewSetSerializer
from rest_framework.views import APIView
from rest_framework.generics import  GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status,permissions
from django.http import HttpResponse, Http404
from django.contrib.auth.models import AbstractBaseUser, UserManager



# # swagger section ###
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


User = get_user_model()

### Logging section  using python only###
# import logging
# # Create logger and configure logger
# LOG_FORMAT ="%(levelname)s: %(asctime)s : %(filename)s: %(funcName)s :%(name)s:%(lineno)d  - %(message)s '"

# logging.basicConfig(filename = './logs/debug.log',
#                     level = logging.DEBUG,
#                     format = LOG_FORMAT, 
                                 
                    
#                     # filemode = 'w',
#                     )
# logger = logging.getLogger() #the name of the logger."logger = logging.getLogger('arsha')" we can use this also.

#### TEST THE LOGGER ####

# logger.info("logger section in python")
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')
# print(logger.level)


# Create simpleapi function 
class simpleapi(APIView):
    permission_classes = (AllowAny,)#AllowAny - anyone can access this function 
    def post(self,request,format = None):
        # logger.info('hai,welcome to DjangoRestFramework.')
        return Response({'text':'hai,welcome to DjangoRestFramework.'},status=status.HTTP_200_OK)


#create  a class for user registration
class RegisterClass(APIView):
    # serializer_class = RegisterSerializer ## at GenericAPIView case only
    permission_classes = (AllowAny,)
#swagger_auto_decorator for APIView :showring  fieldsfor acceptiong user information .
    @swagger_auto_schema(
        operation_description="apiview for register post description ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username','email','password','confirm_password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Register'],
    )

    def post(self,request,format = None):
        serializer = RegisterSerializer(data =request.data) 
        data = {}#create a null dictionary to return the data
        if serializer.is_valid():
            # logger.info('serializer is valid')
            serializedData = serializer.save()
            data['id'] = serializedData.id
            data["Response"]='Registered'
            data['username'] = serializedData.username
            data['email'] = serializedData.email
        else:
            data = serializer.errors # return error if serializer is not valid
            # logger.error('if the serializer is not valid') # error logger 
        
        return Response(data)


# create a class for user login
class LoginClass( APIView):
    permission_classes = (AllowAny,)
    # serializer_class = UserLoginSerializer
    @swagger_auto_schema(
        operation_description="apiview for login post description ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username','password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                
            },
        ),
        security=[],
        tags=['Login'],
    )
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


# permission for specified methods
class UserViewSet(viewsets.ModelViewSet):   
                                                                                                                                                            
    serializer_class = UserViewSetSerializer
    permission_classes_by_action = {        
        'list': (permissions.AllowAny,),#get logger
        'update': (permissions.IsAuthenticated,),#put
        'destroy': (permissions.IsAuthenticated,),#delete
         }

    def get_object(self,pk):
        try:
            return User.objects.get(pk = pk)
        except:
            raise Http404

  
    def list(self,request,pk,format = None):
        userData=self.get_object(pk)
        # userData = User.objects.all()
        # user = request.user.id
        # if userData.id != user:
        #     return Response({'response':'you dont have permission to read single object data.'})
        serializer =UserLoginSerializer(userData)
        return Response(serializer.data)
    
    def update(self, request,pk,  format=None):        
        modify = self.get_object(pk)
        user = request.user.id
        if modify.id != user:
            return Response({'response':'you dont have permission to edit that.'})
        serializer = UserLoginSerializer(modify, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk, format=None):        
        deletedata = self.get_object(pk)
        user = request.user.id
        if deletedata.id != user:
            return Response({'response':'you dont have permission to delete that.'})
        deletedata.delete()
        return Response('successfully deleted the single object',status=status.HTTP_200_OK)

 
    # def get_permissions(self):
    #     try:
    #         # return permission_classes depending on `action` 
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError: 
    #         # action is not set return default permission_classes
    #         return [permission() for permission in self.permission_classes]




# ####### admin have the permission to view and delete user ########

class AdminUserPermission(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk = pk)
        except:
            raise Http404

    def get(self,request,pk):
        if request.user.is_active and request.user.is_superuser:#only the admin can do specific functionality
            # userdata= User.objects.get(id=pk)
            userdata = self.get_object(pk)
            print(userdata)
            return HttpResponse( userdata )     
        else:
            return HttpResponse("Couldn't have the permission to view the user data.")

    def delete(self,request,pk):
        if request.user.is_active and request.user.is_superuser:
            # userdata= User.objects.get(id=pk)
            userdata = self.get_object(pk)
            print(userdata)
            userdata.delete()
            return HttpResponse('Admin deleted the user details .') 
    
        else:
            return HttpResponse("Couldn't have the permission to view the user data.")

    @swagger_auto_schema(       
        request_body=UserViewSetSerializer,        
      )

    def put(self,request,pk):
        if request.user.is_active and request.user.is_superuser:
            userdata = self.get_object(pk)
            serializer = UserLoginSerializer(userdata,data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse("Couldn't have the permission to view the user data.")
