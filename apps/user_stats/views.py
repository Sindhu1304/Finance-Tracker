from django.shortcuts import render
from datetime import timedelta, date

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.expenses.models import Expense, Category
from apps.expenses.serializers import ExpenseSerializer

tags = ["Stats"]


class ExpensesStats(APIView):
    """
            API endpoint to retrieve expense statistics for a user.

            This endpoint allows users to retrieve the total amount spent within a specific
            date range or one week or one month for each expense category or just returns the total amount for each category since the user signed up.

            **Parameters:**

            - `range` (optional, str): The desired date range. Valid options are:
                - `"Today"`: Returns the total amount spent on each category for the current day.
                - `"Ysterday"`: Returns the total amount spent on each category for the previous day.

            **Response:**

            A JSON object with the following structure:

            ```json
            {
                "Category Data": {
                    "category_name_1": total_amount_1,
                    "category_name_2": total_amount_2,
                    # ... and so on for each category
                }
            }
            ```
    """,

    @extend_schema(
        tags=tags,
        summary="Statistics for expenses",
        description="""
            This endpoint returns the total amount spent for each category within the specified range or the total amount the user has spent 
            on each category since they started using the app.
            """,
        parameters=[
            OpenApiParameter(
                name="range",
                type=str,
                required=False,
                description="Date range",
                enum=["Today", "Yesterday", "This week", "This month"],
            ),
            
        ],
    )
    def get(self, request):
        date_range = request.query_params.get("range")
        
        if date_range:
            if date_range.lower() not in [
                "today",
                "yesterday",
                "this week",
                "this month",
            ]:
                return Response(
                    {
                        "error": "Invalid range. Use 'today', 'yesterday', 'this week' or 'this month' "
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        categories = Category.objects.filter(owner=request.user)
        total = {}
        for category in categories:
            expenses = category.expenses.all()
            if date_range:
                start_date, end_date = self.get_date_range(date_range)
                expenses = self.get_expenses_in_range(expenses, start_date, end_date)
            total[category.name] = self.get_category_total(expenses)

        return Response({"Category Data": total})

    def get_date_range(self, date_range):
        today = date.today()

        if date_range.lower() == "today":
            start_date = today
            end_date = start_date

        elif date_range.lower() == "yesterday":
            start_date = today - timedelta(days=1)
            end_date = start_date

        elif date_range.lower() == "this week":
            year = today.year
            month = today.month

            start_date = today - timedelta(today.weekday())
            end_date = today

        elif date_range.lower() == "this month":
            # Get the current year and month
            year = today.year
            month = today.month

            """
               The first date of the month is 1, so we create a date with the current year, month and date
            """
            start_date = 1
            start_date = date(year, month, start_date)
            """
                Set the end date to the current day of the month the user is in... since tomorrow is unknown
            """
            end_date = today

        return start_date, end_date

    def get_category_total(self, expenses):
        amount = 0
        # amount = amount + expenses.amount for expense in expenses
        for expense in expenses:
            amount += expense.amount
        return amount

    def get_expenses_in_range(self, expenses, start_date, end_date):
        data = {}
        expenses_obj = expenses.filter(
            created_at__lte=end_date, created_at__gte=start_date
        )
        return expenses_obj


class TotalExpenses(APIView):
    serializer_class = ExpenseSerializer

    def get(self, request):
        expenses = Expense.objects.filter(owner=request.user)
        total = 0
        for expense in expenses:
            total += expense.amount

        return Response({"total expenses": total}, status=status.HTTP_200_OK)
