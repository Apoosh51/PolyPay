from django.urls import path
from . import views

urlpatterns = [
    path('admin/curator/',            views.admin_curator,   name='admin_curator'),
    path('admin/curator/cancel/<int:pk>/', views.cancel_transfer, name='cancel_transfer'),
    path('student/bank/',             views.student_bank,    name='student_bank'),

    path('student/bank/',                   views.student_bank,  name='student_bank'),
    path('student/bank/ticket/buy/',        views.buy_ticket,    name='buy_ticket'),
    path('student/bank/ticket/use/<int:ticket_id>/', views.use_ticket, name='use_ticket'),
]
