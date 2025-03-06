from django.contrib.admin import ModelAdmin, site
from .models import MessageModel, DialogsModel, UploadedFile, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'phone_number', 'first_name', 'position', 'department', 'per_status', 'dep_id', 'per_id', 'birthday']
    list_filter = ['id', 'per_status', 'department']
    search_fields = ['username', 'first_name', 'last_name', 'per_status', 'department', 'dep_id']


    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )


class MessageModelAdmin(ModelAdmin):
    readonly_fields = ('created', 'modified',)
    search_fields = ('id', 'text', 'sender__pk', 'recipient__pk')
    list_display = ('id', 'sender', 'recipient', 'text', 'file', 'read')
    list_display_links = ('id',)
    list_filter = ('sender', 'recipient')
    date_hierarchy = 'created'




class DialogsModelAdmin(ModelAdmin):
    readonly_fields = ('created', 'modified',)
    search_fields = ('id', 'user1__pk', 'user2__pk')
    list_display = ('id', 'user1', 'user2')
    list_display_links = ('id',)
    date_hierarchy = 'created'


site.register(DialogsModel, DialogsModelAdmin)
site.register(MessageModel, MessageModelAdmin)
site.register(UploadedFile)
admin.site.register(User, CustomUserAdmin)


