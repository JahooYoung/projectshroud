from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from graphene_django.views import GraphQLView
from backend import views

urlpatterns = [
    path('user/', views.UserProfileView.as_view()),
    path('users/<pk>/', views.UserView.as_view()),

    path('event/', views.EventList.as_view()),
    path('event/past/', views.PastEventList.as_view()),
    path('event/ongoing/', views.OngoingEventList.as_view()),
    path('event/future/', views.FutureEventList.as_view()),

    path('reg-conflict/', views.UserEventConflict.as_view()),
    path('register/', views.UserEventRegister.as_view()),
    path('approve/', views.ApproveEventRegister.as_view()),
    path('unregister/', views.UserEventUnregister.as_view()),
    path('assignadmin/', views.AssignEventAdmin.as_view()),

    path('event/admins/', views.UserManageEventList.as_view()),
    path('event/registered/', views.UserRegisterEventList.as_view()),
    path('event/registered/past/', views.UserRegisterPastEventList.as_view()),
    path('event/registered/ongoing/', views.UserRegisterOngoingEventList.as_view()),
    path('event/registered/future/', views.UserRegisterFutureEventList.as_view()),

    path('event/<pk>/', views.EventDetail.as_view()),
    path('event/<pk>/checkin/', views.EventCheckInList.as_view()),
    path('event/<pk>/attendee/', views.EventAttendeeList.as_view()),
    path('event/<pk>/admins/', views.EventAdminList.as_view()),

    path('trans/', views.TransportCreateView.as_view()),
    path('trans/<pk>/', views.TransportView.as_view()),

    path('checkin/<pk>/toggle/', views.ToggleCheckIn.as_view()),
    path('checkin/<pk>/', views.UserCheckInEvent.as_view()),
    path('checkin/<pk>/delete/', views.DeleteCheckIn.as_view()),

    path('dummy/', views.DummyView.as_view()),

    path('qrcode/', views.gen_qrcode),

    # Activation email
    path('activate/', views.activate_user),
    path('send/activation/', views.send_activation),

    path("graphql/", GraphQLView.as_view(graphiql=True)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
