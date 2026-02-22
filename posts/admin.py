from django.contrib import admin
from .models import Post, UserTheme

admin.site.register(UserTheme)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['caption', 'upload_date']
    search_fields = ['caption', 'keywords']
