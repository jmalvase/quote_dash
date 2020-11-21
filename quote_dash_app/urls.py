from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('dash', views.dashboard),
    path('logout', views.logout),
    path('add_quote', views.add_quote),
    path('user/<int:user_id>', views.profile),
    path('delete/<int:quote_id>', views.delete_quote),
    path('like/<int:quote_id>', views.like_quote),
    path('my_account/<int:user_id>', views.edit_profile),
    path('update/<int:profile_id>', views.update_profile)
]