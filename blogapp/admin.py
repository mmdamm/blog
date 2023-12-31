from django.contrib import admin
from .models import *


# inline
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'publish', 'category']
    ordering = ['author', 'title', 'category']
    list_filter = ['author', 'status', 'publish', 'category']
    search_fields = ['status', 'description', 'author', 'category']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status']
    list_display_links = ['author', 'title']
    inlines = [ImageInline, CommentInline]


# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', 'created']
    search_fields = ['created', 'name']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'bio', 'job', 'photo']