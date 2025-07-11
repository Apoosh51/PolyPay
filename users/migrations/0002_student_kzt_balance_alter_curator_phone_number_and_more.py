# Generated by Django 5.2.3 on 2025-06-15 09:50

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='kzt_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='curator',
            name='phone_number',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^\\+7\\d{10}$', 'Номер должен быть в формате +7XXXXXXXXXX')]),
        ),
        migrations.AlterField(
            model_name='curator',
            name='polycoin_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='curator',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='curator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='users.curator'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^\\+7\\d{10}$', 'Номер должен быть в формате +7XXXXXXXXXX')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='polycoin_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
