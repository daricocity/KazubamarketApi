import json
from . import serializers
from accounts.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from KazubamarketApi.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from rest_framework.parsers import MultiPartParser, FormParser
from KazubamarketApi.utils import jwt_response_payload_handler
from rest_framework import status, mixins, permissions, generics, views
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from accounts.api.serializers import UserRegistrationSerializer, UserListSerializer, UserDetailSerializer, ChangePasswordSerializer, UserDetailUpdateSerializer

########## User Change Password API View ##########
class ChangePasswordView(UpdateAPIView):
    """
    Endpoint for User Change Password.
    """
    model = User
    serializer_class = ChangePasswordSerializer
    allowed_methods = ('PUT', 'OPTIONS', 'HEAD')
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)
            
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

########## User List API View ##########    
class UserListAPIView(ListAPIView):
    """
    Endpoint for User List, only viewd by admin.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

########## User Detail Update API View ########## 
class UserDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    Endpoint for User Detail Update.
    """
    allowed_methods = ('PUT', 'OPTIONS', 'HEAD')
    serializer_class = UserDetailUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(User, pk=pk)
        return obj
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

########## User Detail API View ##########
class UserDetailAPIView(RetrieveAPIView):
    """
    Endpoint for User Detail.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        try:  
            qs = User.objects.filter(pk=user_id)
            user_obj = qs
        except User.DoesNotExist:
            return Response({"response":"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return user_obj

########## User Registration API View ##########
class UserRegistrationAPIView(CreateAPIView):
    """
    Endpoint for User registration.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






























# ######### User Login API View ########## 
# class UserLoginAPIView(GenericAPIView):
#     """
#     Endpoint for User Login.      
#     """
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserLoginSerializer
#     allowed_methods = ('POST', 'OPTIONS', 'HEAD')
#     parser_classes = (MultiPartParser, FormParser,)
    
#     def post(self, request):
#         request = self.request
#         context = {}
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         # username = request.body.decode().split(',')[0].split(':')[1].split('"')[1]
#         # password = request.body.decode().split(',')[1].split(':')[1].split('"')[1]
#         user = authenticate(request, username = username, password = password)
#         if user is not None:
#             if user.is_active:
#                 # login(request, user)
#                 try:
#                     token = Token.objects.get(user=user)
#                 except Token.DoesNotExist:
#                     token = Token.objects.create(user=user)
#                 context['response'] = 'Success'
#                 context['pk'] = user.pk
#                 context['token'] = token.key
#         else:
#             context['response'] = 'Error'
#             context['error_message'] = 'Invalid credentials'
#         return Response(context)

# ########## User Login API View ########## 
# class UserLoginAPIView(generics.GenericAPIView):
#     serializer_class = UserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         context = {}
#         serializer = self.get_serializer(data = request.data)
#         serializer.is_valid(raise_exception = False)
#         user = serializer.validated_data
#         print('This is the user: ',user)
#         if user:
#             try:
#                 token = Token.objects.get(user = user)
#             except Token.DoesNotExist:
#                 token = Token.objects.create(user = user)
#             context = {
#                 'user': UserLoginSerializer(user, context = self.get_serializer_context()).data,
#                 'token': token.key
#             }
#         else:
#             context = {
#                 'user': None,
#                 'token': None
#             }
#         return Response(context)

# ######### User Login API View ########## 
# class UserLoginAPIView(GenericAPIView):
#     """
#     Endpoint for User Login.      
#     """
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserLoginSerializer
#     allowed_methods = ('POST', 'OPTIONS', 'HEAD')
#     parser_classes = (MultiPartParser, FormParser,)
    
#     def post(self, request):
#         request = self.request
#         context = {}
#         try:
#             username = request.POST.get("username")
#             password = request.POST.get("password")
#             user = authenticate(request, username = username, password = password)
#             if user is not None:
#                 try:
#                     payload = jwt_payload_handler(user)
#                     token = jwt.encode(payload, settings.SECRET_KEY)
#                     user_details = {}
#                     user_details['username'] = "%s %s" % (user.username)
#                     user_details['token'] = token
#                     user_logged_in.send(sender = user.__class__, request = request, user = user)
#                     return Response(user_details, status = status.HTTP_200_OK)
#                 except Exception as e:
#                     raise e
#             else:
#                 res = {'error': 'can not authenticate with the given credentials or the account has been deactivated'}
#                 return Response(res, status = status.HTTP_403_FORBIDDEN)
#         except KeyError:
#             res = {'error': 'please provide a username and a password'}
#             return Response(res)

# ########## User Registration API View ##########
# class UserRegistrationAPIView(CreateAPIView):
#     """
#     Endpoint for User registration.
#     """
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserRegistrationSerializer
#     allowed_methods = ('POST', 'OPTIONS', 'HEAD')

#     def post(self, request, format=None):
#         serializer = UserRegistrationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)