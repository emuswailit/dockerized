from django.shortcuts import render
from . import serializers, models
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# # PaymentMethods
class PaymentMethodCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new payment method
    """
    name = "paymentmethods-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethods.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user,facility=user.facility)

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
    Authenticated user
    -------------------------------------------
    View listing of payment methods
    """
    name = "paymentmethods-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PaymentMethodSerializer

    queryset = models.PaymentMethods.objects.all()
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
    Authenticated user
    ----------------------------------------
    View details of a payment method
    """
    name = "paymentmethods-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethods.objects.all()
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
    Admin
    ------------------------------
    Update payment method details
    """
    name = "paymentmethods-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethods.objects.all()
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


# class PaymentUpdateAPIView(generics.RetrieveUpdateAPIView):
#     """
#     Payment update
#     """
#     name = "payment-update"
#     permission_classes = (Is,
#                           )
#     serializer_class = serializers.PaymentSerializer
#     queryset = models.Payment.objects.all()
#     lookup_fields = ('pk',)

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj





