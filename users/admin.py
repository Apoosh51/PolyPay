from django.contrib import admin
from .models import Curator, Student

@admin.register(Curator)
class CuratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'polycoin_balance')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    ordering = ('user__last_name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'group', 'course', 'curator', 'polycoin_balance')
    list_filter  = ('group', 'course', 'curator')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    ordering     = ('group', 'user__last_name')
