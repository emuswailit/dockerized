from core.views import FacilitySafeViewMixin
from django.shortcuts import render
from . import serializers, models
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from core import app_permissions
from django.shortcuts import get_object_or_404


# Retail Accout Views
class RetailerAccountsCreateAPIView(generics.CreateAPIView):
    """
    Retail Superintendent
    ------------------------------------------------------
    Create a new retailer account at a selected wholesale

    """
    name = "retaileraccounts-create"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
                          )
    serializer_class = serializers.RetailerAccountsSerializer
    queryset = models.RetailerAccounts.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(RetailerAccountsCreateAPIView,
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
            return Response(data={"message": "Retailer account created successfully.", "retailer-account": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Retailer account not created", "retailer-account": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class RetailRetailerAccountsListAPIView(generics.ListAPIView):
    """
   Retail Superintendent
   ----------------------------------------------
   List of all accounts created in various wholesales for logged on user's facility
    """
    name = "retaileraccounts-list"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
                          )
    serializer_class = serializers.RetailerAccountsSerializer

    queryset = models.RetailerAccounts.objects.all()

    search_fields = ('wholesale__title',
                     )
    ordering_fields = ('wholesale__title', 'id')

    def get_queryset(self):
        return super().get_queryset().filter(facility=self.request.user.facility,)


class WholesaleRetailerAccountsListAPIView(generics.ListAPIView):
    """
   Wholesaler Superintendent
   ----------------------------------------------
   List of all accounts created in various wholesales for logged on user's facility
    """
    name = "retaileraccounts-list"
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.RetailerAccountsSerializer

    queryset = models.RetailerAccounts.objects.all()

    search_fields = ('wholesale__title',
                     )
    ordering_fields = ('wholesale__title', 'id')

    def get_queryset(self):
        # Retrieve only for the logged in user's wholesale
        return super().get_queryset().filter(wholesale=self.request.user.facility,)


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
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.RetailerAccountsUpdateSerializer
    queryset = models.RetailerAccounts.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(RetailerAccountsUpdateAPIView,
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


# Wholesale products views


# class WholesaleProductsCreateAPIView(generics.CreateAPIView):
#     """
#     Wholesale Superintendent
#     ------------------------------------------------------
#     Create a new wholesale product

#     """
#     name = "wholesaleproducts-create"
#     permission_classes = (app_permissions.FacilitySuperintendentPermission,
#                           )
#     serializer_class = serializers.WholesaleProductsSerializer
#     queryset = models.WholesaleProducts.objects.all()

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(owner=user, facility=user.facility)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_create(serializer)
#             return Response(data={"message": "Wholesale product created successfully.", "wholesale-product": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"message": "Wholesale products not created", "wholesale-product": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


# class WholesaleProductsListForWholesaler(generics.ListAPIView):
#     """
#    Authenticated user
#    ----------------------------------------------
#    Wholesale product listing
#     """
#     name = "wholesaleproducts-list"
#     permission_classes = (app_permissions.WholesaleSuperintendentPermission,
#                           )
#     serializer_class = serializers.WholesaleProductsSerializer

#     queryset = models.WholesaleProducts.objects.all()

#     def get_queryset(self):
#         # Filter to return only for facility
#         return super().get_queryset().filter(facility=self.request.user.facility)

#     search_fields = ('product__title',
#                      'product__description', 'product__preparation__title', 'product__preparation__title')
#     ordering_fields = ('product__title', 'id')


# class WholesaleProductsListForRetailer(generics.ListAPIView):
#     """
#    Authenticated user
#    ----------------------------------------------
#    Wholesale product listing
#     """
#     name = "wholesaleproducts-list"
#     permission_classes = (app_permissions.PharmacySuperintendentPermission,
#                           )
#     serializer_class = serializers.WholesaleProductsSerializerForRetailer

#     queryset = models.WholesaleProducts.objects.all()
#     search_fields = ('product__title',
#                      'product__description', 'product__preparation__title', 'product__preparation__title')
#     ordering_fields = ('product__title', 'id')


# class WholesaleProductsDetailAPIView(generics.RetrieveAPIView):
#     """
#     Authenticated  User
#     ---------------------------------------------------------
#     View wholesale product details
#     """
#     name = "wholesaleproducts-detail"
#     permission_classes = (permissions.IsAuthenticated,
#                           )
#     serializer_class = serializers.WholesaleProductsSerializer
#     queryset = models.WholesaleProducts.objects.all()
#     lookup_fields = ('pk',)

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj


# class WholesaleProductsUpdateAPIView(generics.RetrieveUpdateAPIView):
#     """
#     Wholesale Superintendent
#     ------------------------------------------------------------
#     Update a wholesale product entry
#     """
#     name = "wholesaleproducts-update"
#     permission_classes = (app_permissions.FacilitySuperintendentPermission,
#                           )
#     serializer_class = serializers.WholesaleProductsSerializer
#     queryset = models.WholesaleProducts.objects.all()
#     lookup_fields = ('pk',)

#     def get_serializer_context(self):
#         user_pk = self.request.user.id
#         context = super(WholesaleProductsUpdateAPIView,
#                         self).get_serializer_context()

#         context.update({
#             "user_pk": user_pk

#         })
#         return context

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj

#     # Wholesale variations


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


class WholesaleVariationsListForRetailer(generics.ListAPIView):
    """
    Authenticated users
    ------------------------------------------------------
    Listing of all wholesale variations for all wholesales but items which are in stock
    """
    name = "wholesalevariations-list"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.available_wholesale_variations()
    search_fields = ('product__title', 'product__preparation__title',
                     'product__description', 'product__manufacturer__title', 'comment')
    ordering_fields = ('product__title', 'id')


class WholesaleVariationsListForWholesaler(generics.ListAPIView):
    """
    Authenticated users
    ------------------------------------------------------
    Listing of all wholesale variations for a particular wholesale
    """
    name = "wholesalevariations-list"
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.WholesaleVariationsSerializer
    queryset = models.WholesaleVariations.objects.all()
    search_fields = ('product__title', 'product__preparation__title',
                     'product__description', 'product__manufacturer__title', 'comment')
    ordering_fields = ('product__title', 'id')

    def get_queryset(self):
        # Filter to return only for facility
        return super().get_queryset().filter(facility=self.request.user.facility)


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
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
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
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.BonusesSerializer
    queryset = models.Bonuses.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(BonusesCreateAPIView,
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
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.BonusesSerializer
    queryset = models.Bonuses.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(BonusesUpdateAPIView,
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


class DiscountsCreateAPIView(generics.CreateAPIView):
    """
    Facility Superintendent
    ----------------------------------------------
    Create a new discount for a  wholesale product variation 
    """
    name = "discounts-create"
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.DiscountsSerializer
    queryset = models.Discounts.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(DiscountsCreateAPIView,
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
            return Response(data={"message": "Discount created successfully.", "discount": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Discount not created", "discount": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


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
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.DiscountsSerializer
    queryset = models.Discounts.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(DiscountsUpdateAPIView,
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


class RequisitionsCreateAPIView(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Retail Superintendent
    --------------------------------------------------
    Create a new requisition in a selected wholesale pharmacy
    """
    name = "requisitions-create"
    permission_classes = (app_permissions.RetailSuperintendentPermission,
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


class RequisitionsListForRetailer(FacilitySafeViewMixin, generics.ListAPIView):
    """
   Retail Superintendent
   ------------------------------------------------
   View list of requisitions a retail pharmacy has created on different wholesales
    """
    name = "requisitions-list"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionsSerializer

    queryset = models.Requisitions.objects.all()
    search_fields = ('wholesale__title',
                     'status',)
    ordering_fields = (
        'wholesale__title', 'id')

    def get_queryset(self):

        return super().get_queryset().filter(facility=self.request.user.facility)


class RequisitionsListForWholesaler(generics.ListAPIView):
    """
   Wholesale Superintendent
   ------------------------------------------------
   View list of requisitions created on a wholesale
    """
    name = "requisitions-list"
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
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


class RequisitionsUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retail/Wholesale Superintendent
    """
    name = "requisitions-update"
    permission_classes = (permissions.IsAuthenticated, app_permissions.IsOwner,
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


class RetailerConfirmRequisitionAPIView(generics.UpdateAPIView):
    """
    Retail Superintendent
    ------------------------------------------------------------------
    -Confirm that requisition ia sll set 
    -Wholesale superintendent will only be able to view requisitions after retail superntendent confirms
    -Confirmation also creates foundation for payment
    """
    name = "requisitions-update"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionsRetailerConfirmSerializer
    queryset = models.Requisitions.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        requisition_pk = self.kwargs.get("pk")
        context = super(RetailerConfirmRequisitionAPIView,
                        self).get_serializer_context()
        context.update({
            "user_pk": user_pk, "requisition_pk": requisition_pk})
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RequisitionItemsCreateAPIView(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Retail Superintendent
    ---------------------------------------------------------
    Create a wholesale requisition item
    """
    name = "requisitionitems-create"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
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


class RetailerRequisitionItemsListAPIView(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Retail Superintendent
    ---------------------------------------------------
    View list of own requisition items
    """
    name = "requisitionitems-list"
    permission_classes = (app_permissions.RetailSuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionItemsSerializer

    queryset = models.RequisitionItems.objects.draft_requisition_items()
    # TODO : Reuse this for filtering by q.

    def get_queryset(self):

        return super().get_queryset().filter(facility=self.request.user.facility, owner=self.request.user)

    search_fields = ('wholesale_variation__product__title',
                     'wholesale_variation__product__description', 'wholesale_variation__product__manufacturer__title',)
    ordering_fields = (
        'wholesale_variation__product__title', 'id')


class WholesaleRequisitionItemsListAPIView(generics.ListAPIView):
    """
    Wholesale Superintendent
    ---------------------------------------------------
    View list of retailer confirmed items
    """
    name = "requisitionitems-list"
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionItemsSerializer

    queryset = models.RequisitionItems.objects.retailer_confirmed_items()
    # TODO : Reuse this for filtering by q.

    search_fields = ('wholesale_variation__product__title',
                     'wholesale_variation__product__description', 'wholesale_variation__product__manufacturer__title',)
    ordering_fields = (
        'wholesale_variation__product__title', 'id')


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


class RequisitionItemsUpdateAPIView(generics.DestroyAPIView):
    """
    Owner
    ---------------------------------------------------------------
    Update requisition item
    """
    name = "requisitionitems-update"
    permission_classes = (permissions.IsAuthenticated, app_permissions.IsOwner,
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


class RequisitionPaymentsCreateAPIView(generics.CreateAPIView):
    """
    Retailer: Superintendent
    ---------------------------------------------------------
    Create a despatch payment
    """
    name = "requisitionpayments-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RequisitionPaymentsSerializer
    queryset = models.RequisitionPayments.objects.all()

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


class RequisitionPaymentsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ---------------------------------------------------
    View list of despatch payments
    """
    name = "requisitionpayments-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionPaymentsSerializer

    queryset = models.RequisitionPayments.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionPaymentsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RequisitionPaymentsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class RequisitionPaymentsDetailAPIView(generics.RetrieveAPIView):
    """
   Authenticated user
   -------------------------------------------------------
   View details of a despatch payment
    """
    name = "requisitionpayments-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.RequisitionPaymentsSerializer
    queryset = models.RequisitionPayments.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RequisitionPaymentsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Retail Superintendent
    ---------------------------------------------------------------
    -Update requisition payment to SUCCESS
    -Done after succesfull outsourced payment processing e.g mpesa, visa
    -Part of checkout process
    -Load items to retail
    """
    name = "requisitionpayments-update"
    permission_classes = (permissions.IsAuthenticated, app_permissions.IsOwner,
                          )
    serializer_class = serializers.RequisitionPaymentsSerializer
    queryset = models.RequisitionPayments.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        requisition_pk = self.kwargs.get("pk")
        context = super(RequisitionPaymentsUpdateAPIView,
                        self).get_serializer_context()
        context.update({
            "user_pk": user_pk})
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class InvoicesListForRetailer(generics.ListAPIView):
    """
    Authenticated user
    ---------------------------------------------------
    View list of despatch payments
    """
    name = "invoices-list"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
                          )
    serializer_class = serializers.InvoicesSerializer

    queryset = models.Invoices.objects.all()
    search_fields = ('invoice__requisition__wholesale__title', 'invoice__requisition__facility__title'
                     )
    ordering_fields = ('invoice__requisition__wholesale__title', 'id')

    def get_queryset(self):
        return super().get_queryset().filter(facility=self.request.user.facility,)


class InvoicesListForWholesaler(generics.ListAPIView):
    """
    Authenticated user
    ---------------------------------------------------
    View list of despatch payments
    """
    name = "invoices-list"
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.InvoicesSerializer

    queryset = models.Invoices.objects.all()
    search_fields = ('invoice__requisition__wholesale__title', 'invoice__requisition__facility__title'
                     )
    ordering_fields = ('invoice__requisition__wholesale__title', 'id')

    def get_queryset(self):
        return super().get_queryset().filter(wholesale=self.request.user.facility,)


class InvoicesDetailAPIView(generics.RetrieveAPIView):
    """
   Authenticated user
   -------------------------------------------------------
   View details of a despatch payment
    """
    name = "invoices-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.InvoicesSerializer
    queryset = models.Invoices.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class InvoicesUpdateForRetailer(generics.RetrieveUpdateAPIView):
    """
    Retail Superintendent
    ---------------------------------------------------------------
    -Update requisition payment to SUCCESS
    -Done after succesfull outsourced payment processing e.g mpesa, visa
    -Part of checkout process
    -Load items to retail
    """
    name = "invoices-update"
    permission_classes = (app_permissions.PharmacySuperintendentPermission,
                          )
    serializer_class = serializers.InvoicesUpdateSerializerForRetailer
    queryset = models.Invoices.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        requisition_pk = self.kwargs.get("pk")
        context = super(InvoicesUpdateForRetailer,
                        self).get_serializer_context()
        context.update({
            "user_pk": user_pk})
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class InvoicesUpdateForWholesaler(generics.RetrieveUpdateAPIView):
    """
    Retail Superintendent
    ---------------------------------------------------------------
    -Update requisition payment to SUCCESS
    -Done after succesfull outsourced payment processing e.g mpesa, visa
    -Part of checkout process
    -Load items to retail
    """
    name = "invoices-update"
    permission_classes = (app_permissions.WholesaleSuperintendentPermission,
                          )
    serializer_class = serializers.InvoicesUpdateSerializerForWholesaler
    queryset = models.Invoices.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        requisition_pk = self.kwargs.get("pk")
        context = super(InvoicesUpdateForWholesaler,
                        self).get_serializer_context()
        context.update({
            "user_pk": user_pk})
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class InvoicesUpdateForCourier(generics.RetrieveUpdateAPIView):
    """
    Courier
    ---------------------------------------------------------------
    -Update invoice on succesfull delivery

    """
    name = "invoices-update"
    permission_classes = (app_permissions.CourierPermission,
                          )
    serializer_class = serializers.InvoicesUpdateSerializerForCourier
    queryset = models.Invoices.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        requisition_pk = self.kwargs.get("pk")

        context = super(InvoicesUpdateForCourier,
                        self).get_serializer_context()
        context.update({
            "user_pk": user_pk})
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
