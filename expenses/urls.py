from django.urls import path
from .auth import *
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('getdetails/<str:expenses_details>/', home, name='home_exp_details'),  # Expense details
    path('register/', register, name='register'),  # User registration
    path('login/', login, name='login'),  # User login
    path('logout/', logout, name='logout'),  # User logout
    path('balance-sheet/', balance_sheet, name='balance_sheet'),  # View balance sheet
    path('download_balance_sheet/', download_balance_sheet, name='download_balance_sheet'),  # Download balance sheet
    # path('create-expense/', create_expense, name='create_expense'), 
]