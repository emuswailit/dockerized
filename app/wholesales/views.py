from django.shortcuts import render
from . import serializers, models
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from core import app_permissions
from django.shortcuts import get_object_or_404


# Retail Accout Views
class RetailerAccountsCreateAPIView(generics.CreateAPIView):
    """
    Wholesale Superintendent
    ------------------------------------------------------
    Create a new retailer account

    """
    name = "retaileraccounts-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RetailerAccountsSerializer
    queryset = models.RetailerAccounts.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Retailer account created successfully.", "retailer-account": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Retailer account not created", "retailer-account": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class RetailerAccountsListAPIView(generics.ListAPIView):
    """
   Authenticated user
   ----------------------------------------------
   Wholesale product listing
    """
    name = "retaileraccounts-list"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RetailerAccountsSerializer

    queryset = models.RetailerAccounts.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(RetailerAccountsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RetailerAccountsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class RetailerAccountsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated  User
    ---------------------------------------------------------
    View retailer account details
    """
    name = "retaileraccounts-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RetailerAccountsSerializer
    queryset = models.RetailerAccounts.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RetailerAccountsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Wholesale Superintendent
    ------------------------------------------------------------
    Update a retailer account
    """
    name = "retaileraccounts-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RetailerAccountsSerializer
    queryset = models.RetailerAccounts.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Wholesale products views


class WholesaleProductsCreateAPIView(generics.CreateAPIView):
    """
    Wholesale Superintendent
    ------------------------------------------------------
    Create a new wholesale product

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
   Authenticated user
   ----------------------------------------------
   Wholesale product listing
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
    Authenticated  User
    ---------------------------------------------------------
    View wholesale product details
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
    Wholesale Superintendent
    ------------------------------------------------------------
    Update a wholesale product entry
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
    Wholesale Superintendent
    ------------------------------------------------------
    Create a product variation when receiving new inventory
    """
    name = "wholesalevariations-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(WholesaleVariationsCreateAPIView,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

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
    Authenticated users
    ------------------------------------------------------
    Listing of all wholesale variations
    """
    name = "wholesalevariationss-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.all()
    search_fields = ('wholesale_product__product__title',
                     'wholesale_product__product__description', 'wholesale_product__product__manufacturer__title', 'comment')
    ordering_fields = ('wholesale_product__product__title', 'id')

    def get_context_data(self, *args, **kwargs):
        context = super(WholesaleVariationsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context


class WholesaleVariationsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    -----------------------------------------------------------
    Wholesale product variations listing
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
    Wholesale Superintendent
    -------------------------------------------------------------------
    Update wholesale product variation
    """
    name = "wholesalevariations-update"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(WholesaleVariationsUpdateAPIView,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

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
   Wholesale superintendent
   ------------------------------------------------
   Create a new bonus offer
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
    Authenticated user
    -----------------------------------------
    List of all active bonuses
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
   Authenticated user
   --------------------------------------------------
   Bonus details
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
    Facility supenrintendent
    ---------------------------------------------------
    Update bonus
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
    Facility Superintendent
    ----------------------------------------------
    Create a new discount for a  wholesale product variation 
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
    Authenticated user
    --------------------------------------------
    Discounts list
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
    Authenticated user
    --------------------------------------------------
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
    Wholesale Superintendent
    -----------------------------------------------------------
    Update discount
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
    Retail Superintendent
    --------------------------------------------------
    Create a new requisition in a selected wholesale pharmacy
    """
    name = "requisitions-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionsSerializer
    queryset = models.Requisitions.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(RequisitionsCreateAPIView,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Requisition created successfully.", "requisition": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Requisition not created", "requisition": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class RetailerRequisitionsListAPIView(generics.ListAPIView):
    """
   Retail Superintendent
   ------------------------------------------------
   View list of requisitions a retail pharmacy has created on different wholesales
    """
    name = "requisitions-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionsSerializer

    queryset = models.Requisitions.objects.all()

    def get_queryset(self):

        return super().get_queryset().filter(facility=self.request.user.facility)


class WholesalerRequisitionsListAPIView(generics.ListAPIView):
    """
   Wholesale Superintendent
   ------------------------------------------------
   View list of requisitions created on a wholesale
    """
    name = "requisitions-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionsSerializer

    queryset = models.Requisitions.objects.all()

    def get_queryset(self):

        return super().get_queryset().filter(wholesale=self.request.user.facility)


class RequisitionsDetailAPIView(generics.RetrieveAPIView):
    """
    Retail and Wholesale Superintendents
    -----------------------------------------------------
    View details of a wholesale requisition
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
    Retail/Wholesale Superintendent
    """
    name = "requisitions-update"
    permission_classes = (app_permissions.IsOwner,
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
    Retail Superintendent
    ---------------------------------------------------------
    Create a wholesale requisition item
    """
    name = "requisitionitems-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionItemsSerializer
    queryset = models.RequisitionItems.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(RequisitionItemsCreateAPIView,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

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
    Retail/Wholesale Superintendent
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


class RequisitionItemsUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
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
