from django.urls import path
from . import views

urlpatterns=[
    # path('',views.home,name="home"),
    # path('next',views.next,name="next"),
    # path('prev',views.home,name="prev"),

    path('register',views.register,name="register"), 
    path('login/',views.login_view, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
     path('logout/',views.logout_view, name='logout'),
    path('join/',views.join_room, name='join_room'),
    path('accounts/login/', views.login_view, name='login_again'),
    path('',views.home, name='home'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/updated/', views.profile_updated, name='profile_updated'),
    # path('update-profile/', views.update_user_profile, name='update_profile'),
    
]