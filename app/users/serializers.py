from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.serializers import FacilitySafeSerializerMixin
from users.models import FacilityImage
from entities.models import Pharmacist, Courier, Prescriber
from users.models import UserImage
from entities.serializers import PharmacistSerializer, CourierSerializer, PrescriberSerializer
from subscriptions.serializers import SubscriptionSerializer
from subscriptions.models import Subscription

from . import models

User = get_user_model()

class FacilityImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.FacilityImage
        fields = "__all__"
        read_only_fields = (
             'created_by','facility',
        )


class UserImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserImage
        fields = "__all__"
        read_only_fields = (
            'variation', 'created_by', 'owner',
        )


class FacilitySerializer(serializers.ModelSerializer):
    facility_image = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Facility
        fields = ('id', 'title', 'facility_type', 'county', 'town', 'road', 'building',
                  'latitude', 'longitude', 'description', 'is_verified', 'is_subscribed', 'created', 'updated','facility_image')
        read_only_fields = ('is_verified','is_subscribed')
    title = serializers.CharField(

        validators=[UniqueValidator(queryset=models.Facility.objects.all())]
    )

    def get_facility_image(self, obj):
        facility_image = FacilityImage.objects.filter(facility=obj)
        return FacilityImageSerializer(facility_image, context=self.context, many=True).data


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    dependant_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Account
        fields = "__all__"
        # fields = ('id', 'url', 'limit', 'current_balance', 'owner',
        #           'dependant_details', 'created', 'updated')

        read_only_fields = ('owner',
                            )

    def get_dependant_details(self, obj):
        dependant = models.Dependant.objects.filter(account=obj)
        return DependantSerializer(dependant, context=self.context, many=True).data


class UserSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    subscription_details = serializers.SerializerMethodField(
        read_only=True)
    account_details = serializers.SerializerMethodField(
        read_only=True)
    facility_details = serializers.SerializerMethodField(
        read_only=True)
    pharmacist_details = serializers.SerializerMethodField(
        read_only=True)
    prescriber_details = serializers.SerializerMethodField(
        read_only=True)
    courier_details = serializers.SerializerMethodField(
        read_only=True)
    user_image = serializers.SerializerMethodField(
        read_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    # user_images = UserImageSerializer(many=True, read_only=True)
    # portfolio_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.User
        fields = (
            'url',
            'id',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'national_id',
            'gender',
            'phone',
            'date_of_birth',
            'password',
            'confirm_password',
            'user_image',
            'is_staff',
            'is_active',
            'is_pharmacist',
            'is_prescriber',
            'is_superintendent',
            'is_courier',
            'is_client',
            'subscription_details',
            'facility_details',
            'account_details',
            'courier_details',
            'pharmacist_details',
            'prescriber_details',



            # 'portfolio_details',
        )

        read_only_fields = ('is_staff', 'is_active',  'is_pharmacist',
                            'is_prescriber', 'is_superintendent',
                            'is_client', 'is_courier',)
        # Make sure that the password field is never sent back to the client.
        # Make sure that the password field is never sent back to the client.
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}, 'confirm_password': {'write_only': True, 'min_length': 8}
        }

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "Email address is already in use")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "Phone address is already in use")
        return value

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        updated = super().update(instance, validated_data)

        # We save again the user if the password was specified to make sure it's properly hashed.
        if 'password' in validated_data:
            updated.set_password(validated_data['password'])
            updated.save()
        return updated

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password') != data.pop('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data

    def get_facility_details(self, obj):
        if obj.facility:
            facility = models.Facility.objects.filter(id=obj.facility.id)
            return FacilitySerializer(facility, context=self.context, many=True).data
        else:
            return []

    def get_subscription_details(self, obj):
        subscription = Subscription.objects.filter(
            facility=obj.facility)
        return SubscriptionSerializer(subscription, context=self.context, many=True).data

    def get_account_details(self, obj):
        account = models.Account.objects.get(owner=obj)
        return AccountSerializer(account, context=self.context).data

    def get_pharmacist_details(self, obj):
        pharmacist = Pharmacist.objects.filter(owner=obj)
        return PharmacistSerializer(pharmacist, context=self.context, many=True).data

    def get_prescriber_details(self, obj):
        prescriber = Prescriber.objects.filter(owner=obj)
        return PrescriberSerializer(prescriber, context=self.context, many=True).data

    def get_courier_details(self, obj):
        courier = Courier.objects.filter(owner=obj)
        return CourierSerializer(courier, context=self.context, many=True).data
    
    def get_user_image(self, obj):
        user_image = UserImage.objects.filter(owner=obj)
        return UserImageSerializer(user_image, context=self.context, many=True).data


class MerchantSerializer(serializers.Serializer):
    """Serializer that has two nested Serializers: company and user"""

    facility = FacilitySerializer()
    user = UserSerializer()

    def create(self, validated_data):
        facility_data = validated_data['facility']
        user_data = validated_data['user']

        # Call our CompanyManager method to create the Company and the User
        facility, user = models.Facility.objects.create_account(
            facility_title=facility_data.get('title'),
            facility_type=facility_data.get('facility_type'),
            facility_county=facility_data.get('county'),
            facility_town=facility_data.get('town'),
            facility_road=facility_data.get('road'),
            facility_building=facility_data.get('building'),
            facility_latitude=facility_data.get('latitude'),
            facility_longitude=facility_data.get('longitude'),
            facility_description=facility_data.get('description'),
            email=user_data.get('email'),
            phone=user_data.get('phone'),
            first_name=user_data.get('first_name'),
            middle_name=user_data.get('middle_name'),
            last_name=user_data.get('last_name'),
            national_id=user_data.get('national_id'),
            gender=user_data.get('gender'),
            date_of_birth=user_data.get('date_of_birth'),
            password=user_data.get('password'),
            # confirm_password=user_data.get('confirm_password'),
        )

        return {'facility': facility, 'user': user}

    def update(self, instance, validated_data):
        raise NotImplementedError('Cannot call update() here')


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'}, max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('first_name',
                  'last_name')

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "Email address is already in use")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "Phone address is already in use")
        return value


class AllergySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Allergy
        fields = ('id', 'url', 'dependant', 'allergy',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'dependant',
                            'owner', 'created', 'updated')


class DependantSerializer(serializers.HyperlinkedModelSerializer):
    allergy_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Dependant
        fields = ('id', 'url', 'account', 'owner', 'first_name', 'middle_name',
                  'last_name', 'gender', 'date_of_birth', 'allergy_details', 'created', 'updated')

        read_only_fields = ('id', 'url', 'account', 'owner',
                            'created', 'updated')

    def get_allergy_details(self, obj):
        allergy = models.Allergy.objects.filter(dependant=obj)
        return AllergySerializer(allergy, context=self.context, many=True).data

# class PharmacistCertificateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PharmacistCertificate
#         fields = ('id', 'url', 'pharmacist', 'certificate')
#         read_only_fields = (
#             'owner', 'pharmacist',
#         )

# class PharmacistPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PharmacistPhoto
#         fields = "__all__"
#         read_only_fields = ('owner', 'pharmacist')


# class PharmacistSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Pharmacist
#         fields = "__all__"

#         read_only_fields = ('id', 'url', 'cadre',  'is_available',
#                             'is_active', 'is_verified', 'owner', 'created', 'updated', )

# class PharmacistSerializer(serializers.ModelSerializer):
#     pharmacist_photo_details = serializers.SerializerMethodField(
#         read_only=True)

#     class Meta:
#         model = Pharmacist
#         fields = ('id', 'url', 'cadre', 'certificate', 'board_number', 'is_available',
#                   'is_active', 'is_verified', 'owner', 'pharmacist_photo_details', 'created', 'updated', )

#         read_only_fields = ('id', 'url',  'is_available',
#                             'is_active', 'is_verified', 'owner', 'created', 'pharmacist_photo_details', 'updated', )

#     def get_pharmacist_photo_details(self, obj):
#         photo = PharmacistPhoto.objects.filter(pharmacist=obj)
#         return PharmacistPhotoSerializer(photo, context=self.context, many=True).data


# class PharmacistVerifySerializer(serializers.ModelSerializer):
#     """Serializer for setting pharmacist to is verified after due diligence and KYC"""
#     class Meta:
#         model = Pharmacist
#         fields = ('is_verified',)


# class PrescriberPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PrescriberPhoto
#         fields = "__all__"
#         read_only_fields = ('owner', 'prescriber')


# class PrescriberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prescriber
#         fields = ('id', 'url', 'cadre', 'certificate', 'board_number', 'is_available',
#                   'is_active', 'is_verified', 'owner', 'created', 'updated', )

#         read_only_fields = ('id', 'url', 'cadre',  'is_available',
#                             'is_active', 'is_verified', 'owner', 'created', 'updated', )


# class CourierPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourierPhoto
#         fields = "__all__"
#         # fields = (
#         #     'id',
#         #     'url',
#         #     'courier',
#         #     'certificate',
#         #     'owner',
#         #     'created',
#         #     'updated'
#         # )

#         read_only_fields = (
#             'id',
#             'url',
#             'owner',
#             'courier',
#             'created',
#             'updated'
#         )


# class CourierSerializer(serializers.ModelSerializer):
#     owner_details = serializers.SerializerMethodField(
#         read_only=True)
#     courier_certificate_details = serializers.SerializerMethodField(
#         read_only=True)

#     class Meta:
#         model = Courier
#         # fields = "__all__"
#         fields = ('id', 'url', 'vehicle', 'vehicle_number', 'permit_number', 'is_available', 'is_verified', 'owner_details',
#                   'courier_certificate_details', 'created', 'updated')

#         read_only_fields = ('id', 'url', 'user',
#                             'is_available', 'is_verified', 'owner', 'created', 'updated')

#     def get_owner_details(self, obj):
#         owner = User.objects.get(id=obj.owner.id)
#         return UserSerializer(owner, context=self.context).data

#     def get_courier_certificate_details(self, obj):
#         cerificate = CourierPhoto.objects.filter(courier=obj)
#         return CourierPhotoSerializer(cerificate, context=self.context, many=True).data
