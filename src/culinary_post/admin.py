from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import CulinaryPostComment, CulinaryPost, PostLike


admin.site.register(PostLike)


@admin.register(CulinaryPostComment)
class ReviewAdmin(MPTTModelAdmin):
    list_display = ('id', 'text', 'author', 'status', 'post',)
    list_editable = ('status',)


@admin.register(CulinaryPost)
class CulinaryPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'moderator', )
    list_editable = ('moderator',)