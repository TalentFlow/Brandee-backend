from products.models import (Product)
from rest_framework import generics, serializers
from django.conf import settings
from accounts.models import User
from .serializers import UserSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer,RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util,Utils
import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class RegisterUserView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class=RegisterUserSerializer

    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user=User.objects.get(email=user_data['email'])
        print(user)
        email_body='Hi '+user.first_name+' '+user.last_name+'\n'+'<h1>Thanks for Registering.....!!!!!!!</h1>'
        data={'email_body':email_body, 'to_email':user.email, 'email_subject': 'Thanks for Registering','first_name':user.first_name,'last_name':user.last_name}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


        

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    authentication_classes=[]
    permission_classes=[]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email','')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'accounts:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            # redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+'localhost:3000' + relativeLink
            email_body = absurl
                # +"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email, 'first_name':user.first_name, 'last_name':user.last_name,
                    'email_subject': 'Reset your passsword'}
            Utils.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response({'failure': 'No Account found with this email'}, status=status.HTTP_404_NOT_FOUND)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one.', 'status':status.HTTP_401_UNAUTHORIZED})

            return Response({'success':True, 'message':'Credentials Valid', 'uibd64': uidb64, 'token':token})

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one.', 'status':status.HTTP_401_UNAUTHORIZED})



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    authentication_classes = ()
    permission_classes = ()
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Password reset fail'}, status=status.HTTP_400_BAD_REQUEST)

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset=User.objects.all()
    authentication_classes = ()
    permission_classes = ()