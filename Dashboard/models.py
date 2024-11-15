from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def deposit(self, amount):
        """Deposit money into the wallet."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Withdraw money from the wallet."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.save()

    def transfer(self, to_wallet, amount):
        """Transfer money to another user's wallet."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.withdraw(amount)
        to_wallet.deposit(amount)

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.created_at}"

    def save(self, *args, **kwargs):
        if self.transaction_type == 'transfer':
            # Ensure that the wallet belongs to the correct user
            if self.user != self.wallet.user:
                raise ValueError("The transaction's user and wallet owner must match.")
        super().save(*args, **kwargs)
