from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Expenses(models.Model):
    SPLIT_METHODS = [
        ('equal', 'Equal'),
        ('percentage', 'Percentage'),
        ('exact', 'Exact'),
    ] 

    title = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHODS)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class Participant(models.Model):
    
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} owes {self.amount_owed} for {self.expense.description}"