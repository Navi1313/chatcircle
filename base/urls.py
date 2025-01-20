from django.urls import path
from . import views

urlpatterns =  [

    path('logout/', views.logoutUser , name='logout'),
    path('login/',views.loginPage , name = "login"),
    path('register/',views.registerUser , name = "register"),

    path('' , views.home , name = "home"),
    path('room/<str:pk>/' , views.room , name = "room"),

    path('create-room/' , views.create_room, name =  "create-room") ,
    path('update-room/<str:pk>/' , views.update_room ,name = "update-room"),
    path('delete-room/<str:pk>/' , views.delete_room ,name = "delete-room"),
    path('delete-messege/<str:pk>/' , views.delete_messege ,name = "delete-messege"),
    path('profile/<str:pk>/' , views.user_profile , name="user-profile"),
    path('update-user/' , views.update_user , name="update-user"),
    path('topics' , views.topics_page , name = "topics"),
    path('activity' , views.activity_page , name = "activity"),

    
]