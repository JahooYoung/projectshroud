from django.conf.urls import url
from backend.consumers import ImportConsumer

websocket_urlpatterns = [
    url(r'^ws/import/(?P<event_id>[^/]+)/$', ImportConsumer),
]