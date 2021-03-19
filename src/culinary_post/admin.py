from django.contrib import admin
from .models import PostComment, CulinaryPost, PostLike


admin.site.register(PostLike)
admin.site.register(CulinaryPost)
admin.site.register(PostComment)
