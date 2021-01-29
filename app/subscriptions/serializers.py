
from rest_framework import serializers
from . import models
from payments.models import Payment
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import date, timedelta


User = get_user_model()


class PlanSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Plan
        fields = ('id', 'url', 'title', 'description',
                  'price', 'owner', 'created', 'updated')
        read_only_fields = (
            'owner', 'id',
        )


class SubscriptionPaymentsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.SubscriptionPayments
        fields = ('id', 'url', 'facility', 'plan', 'payment_method',
                  'amount', 'narrative', 'status', 'subscription_created', 'created', 'updated')
        read_only_fields = (
            'owner', 'facility', 'id', 'amount', 'narrative', 'status', 'subscription_created',
        )

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        user = User.objects.get(id=user_pk)
        plan = validated_data.pop('plan')
        if plan and user:
            #Facility has already done a trial plan
            if plan.title =='Trial' and user.facility.trial_done == True:
                raise serializers.ValidationError(f"Please select another plan other than trial.")
            subscription_payment = None
            today_payment =None
            start_date = None
            end_date = None
            days = None
            if plan.title == 'Monthly':
                days = 30
            elif plan.title == 'Yearly':
                days = 366
            elif plan.title == 'Trial':
                days = 30
            if models.SubscriptionPayments.objects.filter(
                created__gt=datetime.today(), subscription_created=False).count()>0:
                today_payment = models.SubscriptionPayments.objects.get(
                created__gt=datetime.today(), subscription_created=False)
            if today_payment:
                subscription_payment = today_payment
            else:

                new_subscription_payment = models.SubscriptionPayments.objects.create(
                    plan=plan, amount=plan.price, **validated_data)
                if new_subscription_payment:
                    subscription_payment = new_subscription_payment
                else:
                    raise serializers.ValidationError(
                        "Subscription payment could not be created")
            if subscription_payment:
                if models.Subscription.objects.filter(facility=user.facility, is_active=True).count() > 0:
                    # Retrieve active subscription. Subscription starts when current subscription ends
                    current_subscription = models.Subscription.objects.get(
                        facility=user.facility, is_active=True)
                    start_date = current_subscription.end_date
                    end_date = start_date + timedelta(days=days)
                    current_subscription.is_active = False
                    current_subscription.save()
                else:
                    # No running subscription so subscription starts today
                    start_date = datetime.today()
                    end_date = start_date + timedelta(days=days)
                # Deactivate current subscription
                
                created = models.Subscription.objects.create(
                    facility=user.facility, 
                    owner=user, 
                    subscription_payment=subscription_payment, 
                    is_active=True, 
                    start_date=start_date, 
                    end_date=end_date)
                if created:
                    #Facility no longer eligible for trial
                    if user.facility.trial_done == False:
                        user.facility.trial_done=True
                        user.facility.is_subscribed=True
                        user.facility.save()
                    subscription_payment.subscription_created=True
                    subscription_payment.save()


        else:
            raise serializers.ValidationError(
                f"Plan was not retrieved")
        return subscription_payment


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Subscription
        fields = ('id', 'url', 'facility', 'subscription_payment',
                  'start_date', 'end_date','is_active', 'owner')
        read_only_fields = (
            'facility', 'owner', 'start_date','is_active', 'end_date',
        )

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        user = User.objects.get(id=user_pk)
        subscription_payment = validated_data.pop('subscription_payment')
        # if plan and user and payment_method:
        #     payment = Payment.objects.create(facility=user.facility,owner=user,amount=plan.price, narrative=f"Subscription for {user.facility.title}",payment_method=payment_method)

        #     if payment:
        #         created = models.Subscription.objects.create(facility=payment.facility,owner=payment.owner, plan=plan, payment_method=payment_method)
        # else:
        #     raise serializers.ValidationError(
        #                 f"Plan was not retrieved")
        # return created
