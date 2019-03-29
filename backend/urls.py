from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views

urlpatterns = [
    path('', views.index),
    path('api/event/', views.EventList.as_view()),
    path('api/event/<pk>/', views.EventDetail.as_view()),
    path('api/users/', views.UserList.as_view()),
    path('api/users/<pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)