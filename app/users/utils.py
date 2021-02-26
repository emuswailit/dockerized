import datetime
from django.conf import settings
from django.utils import timezone


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
        'role': user.role,
        'email': user.email,
        'phone': user.phone,
        'gender': user.gender,
        'is_client': user.is_client,
        'is_pharmacist': user.is_pharmacist,
        'is_professional': user.is_professional,
        'is_administrator': user.is_administrator,
        'is_superintendent': user.is_superintendent,
        'is_prescriber': user.is_prescriber,
        'is_courier': user.is_courier,
        'is_staff': user.is_staff,
        'facility_title': user.facility.title,
        'facility_type': user.facility.facility_type
    }
