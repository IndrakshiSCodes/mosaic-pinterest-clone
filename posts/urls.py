from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('upload/', views.upload_post, name='upload_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('category/<str:category_name>/', views.category, name='category'),
     path('signup/', views.signup_view, name='signup'), 
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'), 
    path('theme/<str:theme_name>/', views.change_theme, name='change_theme'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]