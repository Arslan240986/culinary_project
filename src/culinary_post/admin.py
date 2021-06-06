from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import CulinaryPostComment, CulinaryPost, PostLike


admin.site.register(PostLike)
admin.site.register(CulinaryPost)


@admin.register(CulinaryPostComment)
class ReviewAdmin(MPTTModelAdmin):
    list_display = ('id', 'text', 'author', 'status', 'post',)
    list_editable = ('status',)
