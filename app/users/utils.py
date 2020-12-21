import datetime
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from . import models
from . import serializers


expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


def jwt_response_payload_handler(token, user=None, request=None):

    return {

        'token': token,
        'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200),
        'id': user.id,
        'date_of_birth': user.date_of_birth,
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'gender': user.gender,
        'is_client': user.is_client,
        'is_pharmacist': user.is_pharmacist,
        'is_superintendent': user.is_superintendent,
        'is_prescriber': user.is_prescriber,
        'is_courier': user.is_courier,
        'is_staff': user.is_staff,
        # 'facility': user.facility
    }
