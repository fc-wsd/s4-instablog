from django.contrib import admin

from .models import Post
from .models import Category
from .models import Comment
from .models import Tag



class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', )
    list_display_links = ('id', 'title', )
    ordering = ('-id', '-created_at', )
    inlines = [CommentInlineAdmin]
    list_filter = ('title', )
    search_fields = ('content', )
    date_hierarchy = 'created_at'


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
