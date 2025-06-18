from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Curator, Student

class CuratorSignUpForm(UserCreationForm):
    first_name   = forms.CharField(label='Имя', max_length=30)
    last_name    = forms.CharField(label='Фамилия', max_length=150)
    phone_number = forms.CharField(label='Телефон (+7XXXXXXXXXX)', max_length=16)

    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # добавляем class="form-control" всем полям
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        if commit:
            user.save()
            Curator.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number']
            )
        return user


class StudentSignUpForm(UserCreationForm):
    first_name   = forms.CharField(label='Имя', max_length=30)
    last_name    = forms.CharField(label='Фамилия', max_length=150)
    phone_number = forms.CharField(label='Телефон (+7XXXXXXXXXX)', max_length=16)
    group        = forms.CharField(label='Группа', max_length=20)
    course       = forms.IntegerField(label='Курс', min_value=1, max_value=4)
    curator      = forms.ModelChoiceField(queryset=Curator.objects.all(), label='Куратор')

    class Meta(UserCreationForm.Meta):
        model  = User
        fields = (
            'username', 'first_name', 'last_name', 'phone_number',
            'group', 'course', 'curator',
            'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # добавляем class="form-control" всем полям
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                group=self.cleaned_data['group'],
                course=self.cleaned_data['course'],
                curator=self.cleaned_data['curator']
            )
        return user
