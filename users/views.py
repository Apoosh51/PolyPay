from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CuratorSignUpForm, StudentSignUpForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'curator'):
            return reverse_lazy('admin_curator')
        elif hasattr(user, 'student'):
            return reverse_lazy('student_bank')
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')



def register_curator(request):
    if request.method == 'POST':
        form = CuratorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin_curator')
    else:
        form = CuratorSignUpForm()
    return render(request, 'users/register.html', {
        'form': form,
        'user_type': 'curator'
    })


def register_student(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_bank')
    else:
        form = StudentSignUpForm()
    return render(request, 'users/register.html', {
        'form': form,
        'user_type': 'student'
    })
