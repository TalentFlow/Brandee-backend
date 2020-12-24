from rest_framework import serializers
from django.contrib.auth import get_user_model 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler=settings.JWT_AUTH["JWT_RESPONSE_PAYLOAD_HANDLER"]
expire=settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


UserModel = get_user_model()




class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=50,min_length=6, write_only=True)
    
    class Meta:
        model = UserModel
        fields = ( "id", "email", "first_name","last_name", "password", )

    def validate(self, attrs):
        email= attrs.get('email','')
        first_name= attrs.get('first_name','')
        last_name= attrs.get('last_name','')
        return attrs

    def create(self, validated_data):

        user = UserModel.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],

        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50,min_length=6, write_only=True)
    token=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserModel
        fields = ( "id", "email", "first_name","last_name", "password","token" )

    def validate(self, attrs):
        email= attrs.get('email','')
        first_name= attrs.get('first_name','')
        last_name= attrs.get('last_name','')
        return attrs
    
    def get_token(self,obj):
        user=obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):

        user = UserModel.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],

        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)


    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)