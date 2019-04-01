from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views

urlpatterns = [
    path('', views.index),
    path('api/event/', views.EventList.as_view()),
    path('api/event/past/', views.PastEventList.as_view()),
    path('api/event/ongoing/', views.OngoingEventList.as_view()),
    path('api/event/future/', views.FutureEventList.as_view()),

    path('api/register/', views.UserEventRegister.as_view()),
    path('api/assignadmin/', views.AssignEventAdmin.as_view()),

    path('api/event/admins/', views.UserManageEventList.as_view()),
    path('api/event/registered/', views.UserRegisterEventList.as_view()),
    path('api/event/registered/past/', views.UserRegisterPastEventList.as_view()),
    path('api/event/registered/ongoing/', views.UserRegisterOngoingEventList.as_view()),
    path('api/event/registered/future/', views.UserRegisterFutureEventList.as_view()),

    path('api/event/<pk>/', views.EventDetail.as_view()),
    path('api/event/<pk>/checkin/', views.EventCheckInToken.as_view()),
    path('api/event/<pk>/attendee/', views.EventAttendeeList.as_view()),
    path('api/event/<pk>/admins/', views.EventAdminList.as_view()),

    path('api/trans/', views.TransportCreateView.as_view()),
    path('api/trans/<pk>/', views.TransportView.as_view()),

    path('api/checkin/start/', views.StartCheckIn.as_view()),
    path('api/checkin/<pk>/stop/', views.StopCheckIn.as_view()),
    path('api/checkin/<pk>/', views.UserCheckInEvent.as_view())

    # path('api/users/', views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)