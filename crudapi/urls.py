from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path('', views.Home, name='home'),
    path('signin/', views.SigninPage, name='signin'),
    path('login/', views.LoginView, name='loginuser'),
    path('logout/', views.LogoutView, name='logoutuser'),
    path('createcourse/', views.CreateCourse, name='createcourse'),
    path('course/<int:pk>/', views.CourseDetails, name='course'),
    path('edit_course/<int:pk>/', views.EditCourse, name='edit_course'),
    path('enroll/<int:pk>/', views.EnrollCourse, name='enroll'),
    path('api/', views.TaskApi.as_view()),
    path('api/<int:pk>/', views.TaskApi.as_view()),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),

]