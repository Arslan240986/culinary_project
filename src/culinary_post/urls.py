from django.urls import path
from . import views

app_name = 'culinary_post'

urlpatterns = [
    path('', views.post__list_view, name='culinary_post_view'),
    path('detail/<int:pk>', views.CulinaryPostDetailView.as_view(), name='culinary_post_detail_view'),
    path("detail/<int:pk>/<int:number>/", views.CulinaryPostDetailView.as_view(), name='load_more_comments'),
    path('post/add_comment/<int:pk>', views.AddCommentToPost.as_view(), name='post_add_comment'),
    path('post_add/', views.posts_add, name='culinary_post_add'),
    path('liked/', views.like_unlike_post, name='like_post_view'),
    path('delete/<pk>/delete/', views.CulinaryPostDeleteView.as_view(), name='post_delete'),
    path('update/<pk>/update/', views.CulinaryPostUpdateView.as_view(), name='post_update'),
]