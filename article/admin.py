from django.contrib import admin

from .models import Article, Comment

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    list_display = ["title", "author", "created_date"]
    list_display_links = ["title", "created_date"]
    search_fields = ["title", "content"]
    list_filter = ["created_date"]

    class Meta:
        model = Article

@admin.register(Comment)
class ArticleComment(admin.ModelAdmin):
    list_display = ["article", "comment_content", "comment_author"]
    list_display_links = ["article"]
    search_fields = ["article.title"]
    list_filter = ["article", "comment_date"]

    class Meta:
        model = Comment
