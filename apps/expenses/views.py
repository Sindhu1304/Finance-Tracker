from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from datetime import date

from .serializers import (
    ExpenseSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
    CategoryLimitSerializer,
)
from renderers import UserRenderer
from .models import Expense, Category
from .permissions import IsOwner

tags = [
    ["Expenses"],
    ["Category"],
]


class ExpenseListCreateAPIView(APIView, PageNumberPagination):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=tags[0],
        summary="Expenses list",
        description="This endpoint returns all user's expenses",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
        parameters=[
            OpenApiParameter(
                name="page",
                type=int,
                required=False,
                description="Page number",
            ),
            OpenApiParameter(
                name="query",
                type=str,
                required=False,
                description="category name or expense description",
            ),
        ],
    )
    def get(self, request):

        query = self.request.GET.get("query")
        if query == None:
            query = ""

        user = self.request.user
        expenses = Expense.objects.all().filter(
            Q(description__icontains=query), owner=user
        )
        # set the number if objects to be returned per page
        self.page_size = 10
        # from the PageNumberPagination class, paginate the queyset
        result = self.paginate_queryset(expenses, request, view=self)
        # Serialize the paginated resukts
        serializer = self.serializer_class(result, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        tags=tags[0],
        summary="Create expense",
        description="tThis endpoint creates a new expense",
        request=ExpenseSerializer,
        responses={
            201: ExpenseSerializer,
            400: ExpenseSerializer,
        },
    )
    def post(self, request):
        user = self.request.user
        context = {
                "user": user
            }
        serializer = self.serializer_class(context=context, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailAPIView(APIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "slug"

    @extend_schema(
        tags=tags[0],
        summary="Expense detail",
        description="This endpoint retreives the expense details",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
    )
    def get(self, request, slug):
        expense = Expense.objects.get(slug=slug)
        serializer = self.serializer_class(expense)
        return Response(serializer.data)

    @extend_schema(
        tags=tags[0],
        summary="Update detail",
        description="This endpoint updates expense details",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
    )
    def put(self, request, slug):
        expense = Expense.objects.get(slug=slug)
        serializer = self.serializer_class(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=tags[0],
        summary="Delete Expense",
        description="This endpoint deletes an expense",
        request=ExpenseSerializer,
        responses={"200": ExpenseSerializer},
    )
    def delete(self, request, slug):
        expense = Expense.objects.get(slug=slug)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(APIView):
    serializer_class = CategorySerializer

    @extend_schema(
        tags=tags[1],
        summary="Get user's categories",
        description="""
            This endpoint returns a list of all the categories of the authenticated user
            """,
        request=CategorySerializer,
        responses={"200": CategorySerializer},
    )
    def get(self, request):
        user = request.user
        categories = Category.objects.filter(owner=user)
        serializer = self.serializer_class(categories, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=tags[1],
        summary="Create a new category",
        description="""
        This endpoint creates a new category for the authenticated user
        """,
        request=CategorySerializer,
        responses={"201": CategorySerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        
        serializer.save(owner=request.user)

        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(APIView):
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "slug"

    @extend_schema(
        tags=tags[1],
        summary="Category detail",
        description="This endpoint retreives the category details",
        request=CategoryDetailSerializer,
        responses={"200": CategoryDetailSerializer},
    )
    def get(self, request, slug):
        try:
            category = Category.objects.prefetch_related("expenses").get(slug=slug)

            serializer = self.serializer_class(category)
            return Response({"data": serializer.data})
        except Category.DoesNotExist:
            return Response({"error":f'category with the slug "{slug}" not found'})


class CategorySpendLimitAPIView(APIView):
    serializer_class = CategoryLimitSerializer

    @extend_schema(
        tags=tags[1],
        summary="Category Limit",
        description="This endpoint sets the spend limit for a category",
        request=CategoryLimitSerializer,
        responses={"200": CategoryLimitSerializer},
    )
    def patch(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializer = self.serializer_class(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"data": serializer.data})
