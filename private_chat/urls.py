from django.urls import path


from . import views

app_name = 'private_chat'
urlpatterns = [
    path("", views.InboxView.as_view()),
    # path("<slug>/<int:post_num>", views.ThreadView.as_view(), name='chat_room'),
    path("json/<str:slug>/", views.JsonResponsePrivetMessages.as_view(), name='chat_room'),
    path("json/<str:slug>/<int:number>/", views.JsonResponsePrivetMessages.as_view(), name='chat_room_number'),
    path("json/", views.JsonResponsePrivetMessages.as_view(), name='post_chat_room'),
]