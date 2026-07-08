from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_essential = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class LedgerEntry(models.Model):
    ENTRY_TYPE = [('INCOME', 'Income'), ('EXPENSE', 'Expense')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ledger')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=ENTRY_TYPE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']