from django.urls import path
from .views import create_user, retrieve_user_details, add_expense, retrieve_individual_expenses, retrieve_overall_expenses, download_balance_sheet

urlpatterns = [
    path('user/', create_user, name='create_user'),
    path('user/<int:user_id>/', retrieve_user_details, name='retrieve_user_details'),
    path('expense/', add_expense, name='add_expense'),
    path('expenses/user/<int:user_id>/', retrieve_individual_expenses, name='retrieve_individual_expenses'),
    path('expenses/all/', retrieve_overall_expenses, name='retrieve_overall_expenses'),
    path('expenses/download/', download_balance_sheet, name='download_balance_sheet'),
]