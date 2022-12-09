from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_action),
    path('registration/', views.registration),
    path('account/', views.account),
    path('wall/add_entry/', views.wall_add_entry),
    path('wall/entries/', views.wall_entries_list),
    path('friends/', views.friends_list),
    path('exit/', views.account_exit),
    path('friends/potential/', views.friends_potential_list),
    path('friends/add/', views.friends_add_user),
    path('friends/delete/', views.friends_delete_user),
    path('friends/get_messages/', views.get_messages),
    path('friends/send_message/', views.send_messages),
    path('files/', views.files),
    path('files/load/', views.file_load),
    path('files/delete/', views.file_delete),
    path('settings/', views.settings),
]
