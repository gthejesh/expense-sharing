from django.contrib import admin
from .models import User, Expenses, Participant
# Register your models here.
admin.site.register(User)
admin.site.register(Expenses)
admin.site.register(Participant)