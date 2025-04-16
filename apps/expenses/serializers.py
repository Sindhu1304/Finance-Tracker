from rest_framework import serializers
from .models import Expense, Category
from rest_framework.serializers import ValidationError
from rest_framework.response import Response

from django.urls import reverse 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

    def __init__(self, instance=None, data=None, user=None, **kwargs):
        self.user = user 
        super().__init__(instance, data, **kwargs)

    def validate(self, attrs):
        name = attrs.get("name")
        if self.user:
            existing_category = Category.objects.filter(name=name).first()
            if existing_category:
                raise serializers.ValidationError("Category with this name already exists")
        return attrs


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Expense
        fields = ["category", "amount", "description", "owner", "created_at"]

        read_only_fields = ["owner", "created_at"]

    def validate(self, attrs):
        amount = attrs.get("amount")
        if amount <= 0:
            raise ValidationError({"amount": "Amount must be greater than 0"})
        return attrs

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category, created = Category.objects.get_or_create(name=category_data["name"], owner=self.context["user"])

        if float(category.limit) != 00.00:
            limit = float(category.limit)
            total = 0
            for expense in category.expenses.all():
                total += expense.amount
            difference = limit - float(total)
            if difference <= 0:
                raise ValidationError({"error":"Limit hss been reached"})

        return Expense.objects.create(category=category, **validated_data)


class ExpenseInfoSerializer(serializers.ModelSerializer):
    """
    This serializer is used to get minimal details about an expense.
    The serializer is solely for the category detail view where we
    only need the amount and description
    """

    class Meta:
        model = Expense
        fields = ["amount", "description", "created_at"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)
    expenses = ExpenseInfoSerializer(many=True)
    total = serializers.SerializerMethodField(read_only=True)
    difference_from_limit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "name", 
            "limit", 
            "count", 
            "total", 
            "difference_from_limit",  
            "expenses"
        ]

    def get_count(self, obj) -> int:
        return obj.expenses.count()

    def get_total(self, obj) -> int:
        sum = 0
        for expense in obj.expenses.all():
            sum += expense.amount
        return sum

    def get_difference_from_limit(self,obj) -> float:
        limit = obj.limit
        if not limit:
            return 0
        total = self.get_total(obj)

        difference = limit - total
        return float(difference)


class CategoryLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["limit"]
