from django.shortcuts import render
from . import serializers, models
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from core import app_permissions
from django.shortcuts import get_object_or_404
# Create your views here.


class ListingsCreateAPIView(generics.CreateAPIView):
    """
    Post new listings for dependant
    """
    name = "listings-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ListingsSerializer
    queryset = models.Listings.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Listings created successfully.", "listings": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Listings not created", "listings": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ListingsListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "listings-list"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.ListingsSerializer

    queryset = models.Listings.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(ListingsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ListingsListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class ListingsDetailAPIView(generics.RetrieveAPIView):
    """
    Listings details
    """
    name = "listings-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ListingsSerializer
    queryset = models.Listings.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ListingsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Listings update
    """
    name = "listings-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ListingsSerializer
    queryset = models.Listings.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
