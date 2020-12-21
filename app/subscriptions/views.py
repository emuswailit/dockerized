from django.shortcuts import render
from rest_framework import generics, permissions, status
from . import serializers, models
from core.permissions import IsOwner
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.
# # Plans


class PlanCreateAPIView(generics.CreateAPIView):
    """
    Create new plan
    """
    name = "plan-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PlanSerializer
    queryset = models.Plan.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Plan created successfully.", "plan": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Plan not created", "plan": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PlanListAPIView(generics.ListAPIView):
    """
    Plans list
    """
    name = "plan-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PlanSerializer

    queryset = models.Plan.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PlanListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(PlanListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class PlanDetailAPIView(generics.RetrieveAPIView):
    """
    Plan details
    """
    name = "plan-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PlanSerializer
    queryset = models.Plan.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PlanUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Plan update
    """
    name = "plan-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PlanSerializer
    queryset = models.Plan.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# # Payments
class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Create new payment
    """
    name = "payment-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility_id=user.facility.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Payment created successfully.", "payment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Payment not created", "payment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PaymentListAPIView(generics.ListAPIView):
    """
    Payments list
    """
    name = "payment-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PaymentSerializer

    queryset = models.Payment.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(PaymentListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(facility=user.facility)


class PaymentDetailAPIView(generics.RetrieveAPIView):
    """
    Payment details
    """
    name = "payment-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PaymentUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Payment update
    """
    name = "payment-update"
    permission_classes = (IsOwner,
                          )
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# # PaymentMethods
class PaymentMethodCreateAPIView(generics.CreateAPIView):
    """
    Create new payment
    """
    name = "paymentmethod-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethod.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Payment method created successfully.", "payment-method": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Payment method not created", "payment-method": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PaymentMethodListAPIView(generics.ListAPIView):
    """
    PaymentMethods list
    """
    name = "paymentmethod-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PaymentMethodSerializer

    queryset = models.PaymentMethod.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentMethodListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(PaymentMethodListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class PaymentMethodDetailAPIView(generics.RetrieveAPIView):
    """
    PaymentMethod details
    """
    name = "paymentmethod-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethod.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PaymentMethodUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    PaymentMethod update
    """
    name = "paymentmethod-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethod.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# # Subscriptions

class SubscriptionListAPIView(generics.ListAPIView):
    """
    Subscriptions list
    """
    name = "subscription-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SubscriptionSerializer

    queryset = models.Subscription.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(SubscriptionListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(SubscriptionListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class SubscriptionDetailAPIView(generics.RetrieveAPIView):
    """
    Subscription details
    """
    name = "subscription-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.SubscriptionSerializer
    queryset = models.Subscription.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class SubscriptionUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Subscription update
    """
    name = "subscription-update"
    permission_classes = (IsOwner,
                          )
    serializer_class = serializers.SubscriptionSerializer
    queryset = models.Subscription.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
