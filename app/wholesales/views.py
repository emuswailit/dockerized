from django.shortcuts import render
from . import serializers, models
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from core import app_permissions
from django.shortcuts import get_object_or_404
# Create your views here.


class WholesaleProductsCreateAPIView(generics.CreateAPIView):
    """
    Post new wholesaleproducts for dependant
    """
    name = "wholesaleproducts-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleProductsSerializer
    queryset = models.WholesaleProducts.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Wholesale product created successfully.", "wholesale-product": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Wholesale products not created", "wholesale-product": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class WholesaleProductsListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "wholesaleproducts-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.WholesaleProductsSerializer

    queryset = models.WholesaleProducts.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(WholesaleProductsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(WholesaleProductsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class WholesaleProductsDetailAPIView(generics.RetrieveAPIView):
    """
    WholesaleProducts details
    """
    name = "wholesaleproducts-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.WholesaleProductsSerializer
    queryset = models.WholesaleProducts.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class WholesaleProductsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    WholesaleProducts update
    """
    name = "wholesaleproducts-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleProductsSerializer
    queryset = models.WholesaleProducts.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    # Wholesale variations


class WholesaleVariationsCreateAPIView(generics.CreateAPIView):
    """
    Post new wholesaleproducts for dependant
    """
    name = "wholesalevariations-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Wholesale variation created successfully.", "wholesale-variation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Wholesale variations not created", "wholesale-variation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class WholesaleVariationsListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "wholesalevariationss-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer

    queryset = models.WholesaleVariations.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(WholesaleVariationsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(WholesaleVariationsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class WholesaleVariationsDetailAPIView(generics.RetrieveAPIView):
    """
    WholesaleVariations details
    """
    name = "wholesalevariations-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class WholesaleVariationsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    WholesaleVariations update
    """
    name = "wholesalevariations-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

 # Bonuses


class BonusesCreateAPIView(generics.CreateAPIView):
    """
    Post new wholesaleproducts for dependant
    """
    name = "bonuses-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.BonusesSerializer
    queryset = models.Bonuses.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Bonus created successfully.", "bonus": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Bonus not created", "bonus": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class BonusesListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "bonuses-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.BonusesSerializer

    queryset = models.Bonuses.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(BonusesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BonusesListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class BonusesDetailAPIView(generics.RetrieveAPIView):
    """
    Bonuses details
    """
    name = "bonuses-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.BonusesSerializer
    queryset = models.Bonuses.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class BonusesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Bonuses update
    """
    name = "bonuses-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.BonusesSerializer
    queryset = models.Bonuses.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DiscountsCreateAPIView(generics.CreateAPIView):
    """
    Post new wholesaleproducts for dependant
    """
    name = "discounts-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.DiscountsSerializer
    queryset = models.Discounts.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Bonus created successfully.", "bonus": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Bonus not created", "bonus": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DiscountsListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "discounts-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiscountsSerializer

    queryset = models.Discounts.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DiscountsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DiscountsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class DiscountsDetailAPIView(generics.RetrieveAPIView):
    """
    Discounts details
    """
    name = "discounts-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiscountsSerializer
    queryset = models.Discounts.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DiscountsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Discounts update
    """
    name = "discounts-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.DiscountsSerializer
    queryset = models.Discounts.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RequisitionsCreateAPIView(generics.CreateAPIView):
    """
    Post new wholesaleproducts for dependant
    """
    name = "requisitions-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionsSerializer
    queryset = models.Requisitions.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Bonus created successfully.", "bonus": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Bonus not created", "bonus": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class RequisitionsListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "requisitions-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionsSerializer

    queryset = models.Requisitions.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RequisitionsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class RequisitionsDetailAPIView(generics.RetrieveAPIView):
    """
    Requisitions details
    """
    name = "requisitions-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionsSerializer
    queryset = models.Requisitions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RequisitionsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Requisitions update
    """
    name = "requisitions-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionsSerializer
    queryset = models.Requisitions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RequisitionItemsCreateAPIView(generics.CreateAPIView):
    """
    Retailer: Superintendent
    ---------------------------------------------------------
    Create a wholesale requisition item
    """
    name = "requisitionitems-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionItemsSerializer
    queryset = models.RequisitionItems.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Requisition item created successfully.", "requisition-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Requisition item not created", "requisition-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class RequisitionItemsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ---------------------------------------------------
    View list of requisition items
    """
    name = "requisitionitems-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionItemsSerializer

    queryset = models.RequisitionItems.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionItemsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RequisitionItemsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class RequisitionItemsDetailAPIView(generics.RetrieveAPIView):
    """
   Authenticated user
   -------------------------------------------------------
   View details of requisition item
    """
    name = "requisitionitems-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionItemsSerializer
    queryset = models.RequisitionItems.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RequisitionItemsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Owner
    ---------------------------------------------------------------
    Update requisition item
    """
    name = "requisitionitems-update"
    permission_classes = (app_permissions.IsOwner,
                          )
    serializer_class = serializers.RequisitionItemsSerializer
    queryset = models.RequisitionItems.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DespatchesCreateAPIView(generics.CreateAPIView):
    """
    Post new wholesaleproducts for dependant
    """
    name = "despatches-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.DespatchesSerializer
    queryset = models.Despatches.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Despatch created successfully.", "despatch": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Despatch not created", "despatch": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DespatchesListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "despatches-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DespatchesSerializer

    queryset = models.Despatches.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DespatchesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DespatchesListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class DespatchesDetailAPIView(generics.RetrieveAPIView):
    """
    Despatches details
    """
    name = "despatches-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DespatchesSerializer
    queryset = models.Despatches.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DespatchesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Despatches update
    """
    name = "despatches-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.DespatchesSerializer
    queryset = models.Despatches.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DespatchItemsCreateAPIView(generics.CreateAPIView):
    """
    Retailer: Superintendent
    ---------------------------------------------------------
    Create a wholesale despatch item
    """
    name = "despatchitems-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.DespatchItemsSerializer
    queryset = models.DespatchItems.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Despatch item created successfully.", "despatch-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Despatch item not created", "despatch-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DespatchItemsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ---------------------------------------------------
    View list of despatch items
    """
    name = "despatchitems-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DespatchItemsSerializer

    queryset = models.DespatchItems.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DespatchItemsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DespatchItemsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class DespatchItemsDetailAPIView(generics.RetrieveAPIView):
    """
   Authenticated user
   -------------------------------------------------------
   View details of a despatch item
    """
    name = "despatchitems-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DespatchItemsSerializer
    queryset = models.DespatchItems.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DespatchItemsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Owner
    ---------------------------------------------------------------
    Update despatch item
    """
    name = "despatchitems-update"
    permission_classes = (app_permissions.IsOwner,
                          )
    serializer_class = serializers.DespatchItemsSerializer
    queryset = models.DespatchItems.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DespatchPaymentsCreateAPIView(generics.CreateAPIView):
    """
    Retailer: Superintendent
    ---------------------------------------------------------
    Create a despatch payment
    """
    name = "despatchpayments-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.DespatchPaymentsSerializer
    queryset = models.DespatchPayments.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Despatch payment created successfully.", "despatch-payment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Despatch payment not created", "despatch-payment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DespatchPaymentsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ---------------------------------------------------
    View list of despatch payments
    """
    name = "despatchpayments-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DespatchPaymentsSerializer

    queryset = models.DespatchPayments.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DespatchPaymentsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DespatchPaymentsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class DespatchPaymentsDetailAPIView(generics.RetrieveAPIView):
    """
   Authenticated user
   -------------------------------------------------------
   View details of a despatch payment
    """
    name = "despatchpayments-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DespatchPaymentsSerializer
    queryset = models.DespatchPayments.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DespatchPaymentsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Owner
    ---------------------------------------------------------------
    Update despatch payment
    """
    name = "despatchpayments-update"
    permission_classes = (app_permissions.IsOwner,
                          )
    serializer_class = serializers.DespatchPaymentsSerializer
    queryset = models.DespatchPayments.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
