from django.urls import path
from .auth import *
from .views import *

urlpatterns = [
    path('',home, name='home'),
    path('getdetails/<str:expenses_details>/',home, name='home_exp_details'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('balance-sheet/', balance_sheet, name='balance_sheet'),
    path('download_balance_sheet/', download_balance_sheet, name='download_balance_sheet'),
    # path('create-expense/', create_expense, name='create_expense'),
]