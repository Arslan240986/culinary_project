from django.urls import path
from . import views

app_name = 'contact'
urlpatterns = [
    path('subscribe/json/', views.contact_view, name='contact_subscribe'),
    path('edit/', views.edit, name='user_profile'),
    path('personal/<slug>', views.personal_page, name='personal_page'),
    path('personal/dish/book/<slug>', views.user_dish_book, name='user_dish_book'),
    path('personal/dish/book/add/', views.add_dishes, name='add_dishes_to_book'),
    path('personal/my-invites/', views.invites_received_view, name='my_invites_view'),
    path('personal/all-profile/', views.ProfileListView.as_view(), name='all_profiles_view'),
    path('personal/profile-friends-all/<slug>', views.ProfileFriendList.as_view(), name='all_profiles_friends_view'),
    path('personal/to-invite/', views.invite_profiles_list_view, name='invite_profiles_view'),
    path('personal/send-invite/', views.send_invitation, name='send_invitation'),
    path('personal/remove_friend/', views.remove_from_friends, name='remove_from_friend'),
    path('<slug>/', views.UserProfileDetailView.as_view(), name='profile_detail_view' ),
    path('personal/my-invites/accept/', views.accept_invitation, name='accept_invite'),
    path('personal/my-invites/reject/', views.reject_invitation, name='reject_invite'),
]