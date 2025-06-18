# users/models.py
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Curator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(
        max_length=16,
        validators=[RegexValidator(r'^\+7\d{10}$', 'Номер должен быть в формате +7XXXXXXXXXX')],
        unique=True
    )
    polycoin_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.get_full_name()

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(
        max_length=16,
        validators=[RegexValidator(r'^\+7\d{10}$', 'Номер должен быть в формате +7XXXXXXXXXX')],
        unique=True
    )
    group = models.CharField(max_length=20)
    course = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    curator = models.ForeignKey(
        Curator,
        on_delete=models.PROTECT,
        related_name="students"
    )
    polycoin_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    kzt_balance      = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.group = self.group.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.group}, курс {self.course})"
