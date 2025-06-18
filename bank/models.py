from django.conf import settings
from django.db import models
from users.models import Student

class Transfer(models.Model):
    CURRENCY_CHOICES = [
        ('KZT', 'KZT'),
        ('PC',  'PolyCoin'),
    ]

    from_user   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="transfers_sent",
        on_delete=models.CASCADE
    )
    to_student  = models.ForeignKey(
        Student,
        related_name="transfers_received",
        on_delete=models.CASCADE
    )
    amount      = models.DecimalField(max_digits=12, decimal_places=2)
    currency    = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    created_at  = models.DateTimeField(auto_now_add=True)
    canceled    = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.from_user.username} → {self.to_student.user.username}: {self.amount} {self.currency}"


class Ticket(models.Model):
    CURRENCY_CHOICES = [
        ('KZT', 'KZT'),
        ('PC',  'PolyCoin'),
    ]

    student    = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    currency   = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    # 1000 KZT или 100 PC (100 PC × 10₸ = 1000₸)
    amount     = models.DecimalField(max_digits=12, decimal_places=2)
    used       = models.BooleanField(default=False)
    used_at    = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} — талон {self.created_at.date()}"


"""
from django.conf import settings
from django.db import models
from users.models import Student

class Transfer(models.Model):
    CURRENCY_CHOICES = [
        ('KZT', 'KZT'),
        ('PC',  'PolyCoin'),
    ]

    from_user   = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="transfers_sent",
                                    on_delete=models.CASCADE)
    to_student  = models.ForeignKey(Student,
                                    related_name="transfers_received",
                                    on_delete=models.CASCADE)
    amount      = models.DecimalField(max_digits=12, decimal_places=2)
    currency    = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    created_at  = models.DateTimeField(auto_now_add=True)
    canceled    = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.from_user.username} → {self.to_student.user.username}: {self.amount} {self.currency}"
"""