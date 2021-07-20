from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode as uid_decoder

from sekolah import models


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']
        write_only_fields = ['password', 'password2']

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise serializers.ValidationError('Email address is already in use')

    def validate(self, data):
        password1 = data['password']
        password2 = data.pop('password2')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({'password': "Password doesn't match"})

        return super().validate(data)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        models.Student.objects.create(user=user)

        return user


class LoginSerializer(jwt_serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        if user.student.group:
            token['group'] = user.student.group.name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['refresh_expires'] = refresh['exp']
        data['access'] = str(refresh.access_token)
        data['access_expires'] = refresh.access_token['exp']

        return data


class RefreshTokenSerializer(jwt_serializers.TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = super().validate(attrs)
        data['access_expires'] = refresh.access_token['exp']

        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_form = None

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Email address is not associated with a user')

        self.reset_form = PasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return email

    def save(self):
        request = self.context.get('request')

        opts = {
            'use_https': request.is_secure(),
            'from_email': settings.EMAIL_HOST_USER,
            'request': request,
        }

        self.reset_form.save(**opts, email_template_name='password_reset_email.html')


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128, style={'input_type': 'password'})
    new_password2 = serializers.CharField(max_length=128, style={'input_type': 'password'})

    user = None
    set_password_form = None

    def validate(self, attrs):
        request = self.context.get('request')

        attrs['uid'] = request.parser_context['kwargs'].get('uidb64')
        attrs['token'] = request.parser_context['kwargs'].get('token')

        # Decode the uidb64 (allauth use base36) to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError({'token': ['Invalid value']})

        # Construct SetPasswordForm instance
        self.set_password_form = SetPasswordForm(user=self.user, data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        return self.set_password_form.save()
