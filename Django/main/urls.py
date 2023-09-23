from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('hostel/',views.hostel,name="hostel"),
    path('create_post/',views.create_post,name="create_post"),
    path('query/',views.query,name="query"),
    path('poll/',views.poll,name="poll"),
    path('profile/',views.profile,name = "profile"),
    path('shop/',views.shop,name="shop"),
]