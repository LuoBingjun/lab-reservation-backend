from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin
from api.models import User, Machine, Operator, ReserveRecord, UserGroup, UseRecord, BreachRecord

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone']
    search_fields = ['id', 'email']

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'max_reserve']

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(ReserveRecord)
class ReserveRecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['__str__','user', 'operator', 'date', 'time', 'note', 'checked']
    list_filter = ['date', 'checked']
    search_fields = ['user__username', 'operator__id', 'operator__name']

@admin.register(UseRecord)
class UseRecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_time'
    list_display = ['__str__', 'machine', 'user', 'operator', 'start_time', 'end_time', 'note']
    list_filter = ['machine', 'start_time']
    search_fields = ['user__username', 'operator__id', 'operator__name']

@admin.register(BreachRecord)
class BreachRecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['__str__','user', 'operator', 'date', 'time', 'note']
    list_filter = ['date']
    search_fields = ['user__username', 'operator__id', 'operator__name']

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'available', 'note']
    list_filter = ['available']

admin.site.site_header = '预约平台管理'
admin.site.site_title = '预约平台管理'
admin.site.empty_value_display = '空'