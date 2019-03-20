from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views

urlpatterns = [
    # path('event/', views.event_list),
    # path('event/<int:pk>', views.event_detail),
    path('', views.index),
    path('event/', views.EventList.as_view()),
    path('event/<int:pk>', views.EventDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)