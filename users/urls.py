from django.urls import path
from .views import (
    CustomLoginView, CustomLogoutView,
    register_curator, register_student
)

urlpatterns = [
    path('login/',  CustomLoginView.as_view(),  name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/curator/', register_curator, name='register_curator'),
    path('register/student/', register_student, name='register_student'),
]
