import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from backend.views import check_is_admin
from backend.models import Event

class ImportConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        event_id = self.scope['url_route']['kwargs']['event_id']
        try:
            event = Event.objects.get(pk=event_id)
        except Exception:
            self.close()
        if not check_is_admin(user, event):
            self.close()

        self.group_name = 'event_%s_import' % event_id
        # Join group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.group_name,
    #         {
    #             'type': 'import_message',
    #             'message': self.user.real_name + ': ' + message
    #         }
    #     )

    # Receive message from room group
    def import_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))