from django.shortcuts import render
from . import serializers, models
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from core import app_permissions
from django.shortcuts import get_object_or_404
# Create your views here.


class CategoriesCreateAPIView(generics.CreateAPIView):
    """
    Post new categories for dependant
    """
    name = "categories-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.CategorySerializer
    queryset = models.Categories.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code":0,"response_message": "Categories created successfully.", "obj": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "Categories not created", 
            "obj": serializer.data,  "errors": errors_messages}, status=status.HTTP_400_BAD_REQUEST)


class CategoriesListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "categories-list"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.CategorySerializer

    queryset = models.Categories.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(CategoriesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(CategoriesListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class CategoriesDetailAPIView(generics.RetrieveAPIView):
    """
    Categories details
    """
    name = "categories-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.CategorySerializer
    queryset = models.Categories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class CategoriesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Categories update
    """
    name = "categories-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.CategorySerializer
    queryset = models.Categories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Category entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Category entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

class SubCategoriesCreateAPIView(generics.CreateAPIView):
    """
    Post new categories for dependant
    """
    name = "subcategories-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SubCategorySerializer
    queryset = models.SubCategories.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code":0,"response_message": "Sub category created successfully.", 
            "obj": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "Sub category not created", 
            "obj": serializer.data,  "errors": errors_messages}, status=status.HTTP_400_BAD_REQUEST)


class SubCategoriesListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "subcategories-list"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.SubCategorySerializer

    queryset = models.SubCategories.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(SubCategoriesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(SubCategoriesListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class SubCategoriesDetailAPIView(generics.RetrieveAPIView):
    """
    SubCategories details
    """
    name = "subcategories-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SubCategorySerializer
    queryset = models.SubCategories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class SubCategoriesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    SubCategories update
    """
    name = "subcategories-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SubCategorySerializer
    queryset = models.SubCategories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Sub category entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Sub category entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)