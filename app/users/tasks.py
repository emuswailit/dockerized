from __future__ import absolute_import, unicode_literals
from django.template.loader import render_to_string
from celery import shared_task
import time
from mobipharma_project.celery import app
from users.token_generator import account_activation_token
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from users.models import Facility


@shared_task
def check_subscription_status():
    # time.sleep(10)
   for user in get_user_model().objects.all():
        user_facility = Facility.objects.get(id=user.facility_id)
        if user_facility.is_subscribed:
           print(f"{ user.email} is subscribed!")
        #    user.is_active=False
        #    user.save()
        else:
            user.is_active=False
            user.save()
            print(f"{ user.email} is not subscribed! Will be deactivated")


# @app.task
# def send_verification_email(user_id):
#     UserModel = get_user_model()
#     try:
#         user = UserModel.objects.get(pk=user_id)
      
#            # Send email
#         # if Site._meta.installed:
#         #     current_site = Site.objects.get_current()
#         # current_site = get_current_site(request)
#         email_subject = 'Activate Your Account'
#         message = render_to_string('activate_account.html', {
#             'user': user,
#             'domain': '212.22.173.231',
#             'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
#             'token': account_activation_token.make_token(user),
#         })
#         to_email = user.email
#         email = EmailMessage(email_subject, message, to=[to_email])
#         email.send()
#     except UserModel.DoesNotExist:
#         logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)

