import random

import jwt
import pyotp
import base64
from datetime import datetime

from django.contrib.auth import user_logged_in
from rest_framework_jwt.serializers import jwt_payload_handler

from config import settings
from product_shop.accounts.helpers.smsc_api import *

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User, OTPLogin
from .serializers import RegisterSerializer, OTPLoginSerializer
from django.core.exceptions import ObjectDoesNotExist


def generate_pin():
    upper_limit = 10 ** 4
    pin = random.randint(0, upper_limit - 1)
    return "{:0{length}d}".format(pin, length=4)


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = User.objects.get(phone_number=request.user.phone_number)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'email': user_profile.email
                }]
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


class OTPLoginView(APIView):
    @staticmethod
    def get(request, phone):
        try:
            Mobile = OTPLogin.objects.get(mobile_phone=phone)
        except ObjectDoesNotExist:
            OTPLogin.objects.create(mobile_phone=phone, )
            Mobile = OTPLogin.objects.get(mobile_phone=phone)  # user Newly created Model
        Mobile.counter += 1  # Update Counter At every Call
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        verify_code = OTP.at(Mobile.counter)
        sms = SMSC()
        sms.send_sms(phone, verify_code)
        return Response({"OTP": OTP.at(Mobile.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = OTPLogin.objects.get(mobile_phone=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        print(key)
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            print(Mobile)
            Mobile.is_verified = True
            Mobile.save()
            # payload = jwt_payload_handler(Mobile)
            # token = jwt.encode(payload, settings.SECRET_KEY)
            # user_details = {}
            # user_details['name'] = "%s %s" % (Mobile.first_name, Mobile.last_name)
            # user_details['token'] = token
            # user_logged_in.send(sender=Mobile.__class__,
            #                     request=request, user=Mobile)
            # return Response(user_details, status=status.HTTP_200_OK)

            return Response(key, status=200)

        return Response("OTP is wrong", status=400)
