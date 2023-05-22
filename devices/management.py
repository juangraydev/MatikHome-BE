import logging
import jwt
from core.repository.repository import Repository
from core.repository.repository import Module
from django.db.models import Q as QueryFilter, Value
from core.constants import identifer as idf
from devices.models import *
from devices.serializers import *
import json
from django.conf import settings
from core.util.custom_exceptions import *


from core.util import common
from core.auth.token_authentication import TokenAuthentication

class DevicesManagement(Repository):
    """
    Handles CRUD Logic Functionalities for User
    """

    def __init__(self):
        
        module = Module(name="Devices",
                        model=Devices,
                        serializer=DevicesSerializer)
        super().__init__(module=module)
    
    def find_all(self):
        resp_data = []
        try:
            resp_data = super().find_all()
        except Exception as error:
            print("[Error]")
        
        return resp_data
    
    def find_by_key(self, key):
        resp_data = []
        try:
            criteria = QueryFilter(key=key)
            response = super().find_by_criteria(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)[0]
            print("[Error] Devices FOund")
        except Exception as error:
            print("[Error] Devices Not FOund")
            raise error
        return resp_data
    
    def find_by_homeId_roomId(self, home_id, room_id):
        resp_data = []

        criteria = []
        try:
            
            criteria = QueryFilter(home=home_id)
            
            response = super().find_by_criteria(criteria)
            resp_device = common.get_value(idf.SERIALIZED, response)

            for device in resp_device:
                channel_management = ChannelsManagement()
                channel_resp = channel_management.find_by_device_id_room_id(device_id=device['id'], room_id=room_id)
                for channel in channel_resp:
                    resp_data.append(channel)

            print("channel_resp",resp_data)
                

        except Exception as error:
            print("[Error] Devices Not FOund")
            print(error)
            raise error
        return resp_data
    


class ChannelsManagement(Repository):
    """
    Handles CRUD Logic Functionalities for Rooms
    """

    def __init__(self):
        
        module = Module(name="Channels",
                        model=Channels,
                        serializer=ChannelsSerializer)
        super().__init__(module=module)


    def find_by_device_id_room_id(self, device_id, room_id):
        criteria = []
        if(room_id == "ALL"):
            criteria = QueryFilter(device=device_id)
        else:
            criteria = QueryFilter(device=device_id, room=room_id)
        
         
        response = super().find_by_criteria(criteria)
        channel_resp = common.get_value(idf.SERIALIZED, response)
        return channel_resp

    def update_by_id(self, id, status):
        try: 
            criteria = QueryFilter(id=id)
            response = self.find_by_criteria(criteria)
            instance = common.get_value(idf.INSTANCES, response)[0]

            updated={
                idf.STATUS: json.dumps({"on": status})
            }

            updated[idf.STATUS]=json.dumps({"on": status})
            update_save = super().update(updated, instance)

            print("update_save",update_save)
        except Exception as error:
            print("error",error)


    def find_by_id_esp(self, id):
        criteria = QueryFilter(device=id)
        channel_resp = []
        response = super().find_by_criteria(criteria)
        channels = common.get_value(idf.SERIALIZED, response)
        for channel in channels:
            channel_resp.append(json.loads(channel['status']))
        return {"channels": channel_resp}