from django.contrib import admin

from django.contrib import admin
from .models import SimplePost, CustomUser, Like


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_active', 'last_login', 'last_request']
    list_display_links = ('email', 'username')
    search_fields = ['email', 'username']


admin.site.register(CustomUser, CustomUserAdmin)


class SimplePostAdmin(admin.ModelAdmin):
    model = SimplePost
    search_fields = ['author', 'title', 'content', 'created']
    list_display = ['id', 'author', 'title', 'content', 'created']
    list_filter = ['author']


admin.site.register(SimplePost, SimplePostAdmin)


class LikeAdmin(admin.ModelAdmin):
    model = Like
    search_fields = ['author', 'post', 'created']
    list_display = ['id', 'author', 'post', 'created']
    list_filter = ['author', 'post']


admin.site.register(Like, LikeAdmin)

