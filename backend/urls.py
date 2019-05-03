from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views

urlpatterns = [
    re_path(r'^(?:[^a].*|a[^p].*|ap[^i].*|api[^/].*)$', views.index),
    path('api/user/', views.UserProfileView.as_view()),
    path('api/users/<pk>/', views.UserView.as_view()),

    path('api/event/', views.EventList.as_view()),
    path('api/event/past/', views.PastEventList.as_view()),
    path('api/event/ongoing/', views.OngoingEventList.as_view()),
    path('api/event/future/', views.FutureEventList.as_view()),

    path('api/register/', views.UserEventRegister.as_view()),
    path('api/approve/', views.ApproveEventRegister.as_view()),
    path('api/unregister/', views.UserEventUnregister.as_view()),
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
    path('api/checkin/<pk>/', views.UserCheckInEvent.as_view()),

    path('api/dummy/', views.DummyView.as_view()),

    path('api/qrcode/', views.gen_qrcode),

    # Activation email
    path('api/activate/', views.activate_user),
    path('api/send/activation/', views.send_activation)
]

urlpatterns = format_suffix_patterns(urlpatterns)
