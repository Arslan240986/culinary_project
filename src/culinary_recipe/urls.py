from django.urls import path
from . import views


app_name = 'culinary_recipe'
urlpatterns = [
    path('', views.CategoryViewList.as_view(), name='home'),
    path('ajax/', views.get_ajax_response_category, name='get_ajax_response_category'),
    path('dishes/', views.GetItems.as_view(), name='dishes'),
    path('dishes/by_search/', views.Search.as_view(), name='search_dishes'),
    path('dishes/by_search/<int:page_num>', views.Search.as_view(), name='search_pagination'),
    path('dishes/by_search_title/', views.SearchByTitle.as_view(), name='search_dishes_by_title'),
    path('dishes/add_recipe/', views.DishCreateView.as_view(), name='add_recipe'),
    path('dishes/update_dish/<slug:slug>/', views.DishUpdateView.as_view(), name='update_meal'),
    path('dishes/delete_dish/<int:pk>/', views.DishDeleteView.as_view(), name='delete_meal'),
    path('detail/<slug:slug>/<int:pk>', views.MealDetailView.as_view(), name='detail_view'),
    path("detail/<str:slug>/<int:pk>/<int:number>/", views.MealDetailView.as_view(), name='load_more_comments'),
    path('review/<int:pk>/', views.AddCommentToDish.as_view(), name='add_review'),
    path('recipe/dishes/<slug:slug>/', views.GetItems.as_view(), name='last_list'),
    path('likes_meal/', views.like_unlike_post, name='likes_meal'),
    path('json/', views.ingredient_list_view, name='get_ingredient_lists'),
    path('category/country/<slug:country>/<int:pk>', views.GetItems.as_view(), name='by_country'),
    path('<slug:slug>/', views.get_sub_category, name='cats_list'),
]