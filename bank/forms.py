from django import forms
from users.models import Student

class CreditForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        label='Студент',
        widget=forms.Select(attrs={'class':'form-select'})
    )
    amount  = forms.DecimalField(
        label='Сумма PolyCoin',
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )

class TransferForm(forms.Form):
    phone    = forms.CharField(
        label='Телефон получателя (+7XXXXXXXXXX)',
        max_length=16,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    amount   = forms.DecimalField(
        label='Сумма',
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )
    currency = forms.ChoiceField(
        label='Валюта',
        choices=[('KZT','KZT'), ('PC','PolyCoin')],
        widget=forms.Select(attrs={'class':'form-select'})
    )

class ConversionForm(forms.Form):
    direction = forms.ChoiceField(
        label='Направление конвертации',
        choices=[
            ('pc_to_kzt', 'PolyCoin → KZT'),
            ('kzt_to_pc', 'KZT → PolyCoin'),
        ],
        widget=forms.Select(attrs={'class':'form-select'})
    )
    amount = forms.DecimalField(
        label='Сумма',
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )
