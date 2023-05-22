import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from devices.management import DevicesManagement, ChannelsManagement

class DeviceConsumer(WebsocketConsumer):

    def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.home_id = self.scope['url_route']['kwargs']['home_id']
            self.home_room_group_name = 'homegroup_{0}_{1}'.format(self.home_id,self.room_id)

            async_to_sync(self.channel_layer.group_add)(self.home_room_group_name, self.channel_name)
            
            self.accept()
            device_channel_list = DevicesManagement().find_by_homeId_roomId(home_id=self.home_id, room_id=self.room_id)

            self.send(text_data=json.dumps({
                'type':'deviceInfo',
                'deviceStatus': device_channel_list
            }))
        except:
            print("error lang")
        
        # await self.send(text_data=json.dumps({
        #     'type':'initialized',
        #     'message':"success"
        # }))


    # def receive(self, text_data=None):
    #     data = json.loads(text_data)
    #     message = data['message']
        
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.home_room_group_name,
    #         {
    #             'type':'chat_message',
    #             'message':message
    #         }
            
    #     )

    # def chat_message(self, event):
    #     message = event['message']

    #     self.send(text_data=json.dumps({
    #         'type':'chat',
    #         'message':message
    #     }))

    def receive(self, text_data=None):
        data = json.loads(text_data)
        channelId = data['channelId']
        status = data['status']
        ChannelsManagement().update_by_id(id=channelId, status=status)
        
        async_to_sync(self.channel_layer.group_send)(
            self.home_room_group_name,
            {
                'type':'device_message',
                'deviceStatus': {}
            }
            
        )

    def device_message(self, event):
        device_channel_list = DevicesManagement().find_by_homeId_roomId(home_id=self.home_id, room_id=self.room_id)
        self.send(text_data=json.dumps({
            'type':'deviceInfo',
            'deviceStatus': device_channel_list
        }))


    # def disconnect(self, code):
    #     async_to_sync(self.channel_layer.group_discard)(self.home_room_group_name, self.channel_name)

    # async def onOpen_message(self):

    #     await self.send(text_data=json.dumps({
    #         "data":{
    #             "home": 1,
    #             "room": 2,
    #             "devices": [
    #                 {
    #                     "id": 1,
    #                     "key": 123,
    #                     "type": "control",
    #                     "status": [
    #                         {"value": True}
    #                     ]
    #                 }
    #             ]
    #         }
    #     }))