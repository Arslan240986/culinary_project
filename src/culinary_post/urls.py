from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_comment_create_and_list_view, name='culinary_post_view'),
    path('post_add/', views.posts_add, name='culinary_post_add'),
    path('liked', views.like_unlike_post, name='like_post_view'),
    path('<pk>/delete/', views.CulinaryPostDeleteView.as_view(), name='post_delete'),
    path('<pk>/update/', views.CulinaryPostUpdateView.as_view(), name='post_update'),
]