from django.db import models
from django.contrib.auth.models import User

class Household(models.Model):
    name = models.CharField(max_length=100)
    invite_code = models.CharField(max_length=12, unique=True)
    members = models.ManyToManyField(User, related_name='households')

    def __str__(self):
        return self.name

class SharedExpense(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='shared_expenses')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    title = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(SharedExpense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)

class Chore(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='chores')
    title = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    proof_image = models.ImageField(upload_to='chore_proofs/', null=True, blank=True)
    karma_points = models.IntegerField(default=10)