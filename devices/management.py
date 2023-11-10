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
import uuid
# from socketIO_client import SocketIO



from core.util import common
from core.auth.token_authentication import TokenAuthentication
# from homes.management import HomesManagement

class DevicesManagement(Repository):
    """
    Handles CRUD Logic Functionalities for User
    """

    def __init__(self):
        
        module = Module(name="Devices",
                        model=Devices,
                        serializer=DevicesSerializer)
        super().__init__(module=module)

    def create_device(self, data):
        saved = {}
        channel_mgnt = ChannelsManagement()
        try:
            save_data = {       
                'key': data['key'],
                'home': data['home_id'],
                'type': data['device_type']

            }
            saved = super().save(save_data)

            if(data['device_type'] == 1):
                channel_mgnt.createTempChannel(saved)
            elif(data['device_type'] == 2):
                channel_mgnt.createChannels(saved, data['channel'])
            elif(data['device_type'] == 3):
                channel_mgnt.createChannels(saved, data['channel'])

            

        except Exception as exception:
            print("[Error]", exception)
            raise exception
        
        return saved
    
    def update_device(self, data):
        resp_data = []
        try:
            criteria = QueryFilter(id=data['id'])
            response = super().find_by_criteria(criteria)
            instance = common.get_value(idf.INSTANCES, response)[0]
            save_data = {
                'id': data['id'],
                'key': data['key'],
                'home': data['home_id']
            }
            resp_data = super().update(save_data, instance)

        except Exception as err:
            raise err


        return resp_data
    
    def find_all(self):
        from homes.management import HomesManagement
        resp_data = []
        home_management = HomesManagement()
        channel_management = ChannelsManagement()
        try:
            resp_data = super().find_all()
            
            for device in resp_data:
                channel = channel_management.find_by_device_id(device['id'])
                device['channel'] = len(channel)
                device['home']
                if device['home']:
                    home = home_management.get_house_list_by_id( device['home'].hex)
                    device['home'] = home
                    device['home_id'] = home['id']
                    print(device['home'])

            
        except Exception as error:
            print("[Error]", error)
        
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
    
    def find_by_all_temp_homeId(self, home_id):
        from homes.management import RoomManagement
        resp_data = []
        criteria = []
        try:
            
            criteria = QueryFilter(home=home_id, type=1)
            
            response = super().find_by_criteria(criteria)
            resp_device = common.get_value(idf.SERIALIZED, response)

            for device in resp_device:
                channel_management = ChannelsManagement()
                channel_resp = channel_management.find_by_device_id(device_id=device['id'])
                for channel in channel_resp:
                    room_management = RoomManagement()
                    room = room_management.find_by_id(id=channel['room'])
                    channel['id'] = str(channel['id'])
                    channel['device'] = str(channel['device'])
                    channel['key'] = str(device['key'])
                    channel['status'] = str(channel['status'])
                    channel['room'] = []
                    if(len(room)):
                        channel['room'] = room[0]
                    resp_data.append(channel)

        except Exception as error:
            print("[Error] Devices Not FOund")
            print(error)
            raise error
        return resp_data
    


    def find_by_all_homeId(self, home_id):
        from homes.management import RoomManagement
        resp_data = []
        criteria = []
        try:
            
            criteria = QueryFilter(home=home_id)
            
            response = super().find_by_criteria(criteria)
            resp_device = common.get_value(idf.SERIALIZED, response)

            for device in resp_device:
                channel_management = ChannelsManagement()
                channel_resp = channel_management.find_by_device_id(device_id=device['id'])
                for channel in channel_resp:
                    room_management = RoomManagement()
                    room = room_management.find_by_id(id=channel['room'])
                    channel['id'] = str(channel['id'])
                    channel['device'] = str(channel['device'])
                    channel['key'] = str(device['key'])
                    channel['room'] = []
                    if(len(room)):
                        channel['room'] = room[0]
                    resp_data.append(channel)

        except Exception as error:
            print("[Error] Devices Not FOund")
            print(error)
            raise error
        return resp_data
    
    def find_by_homeId(self, home_id):
        resp_data = []
        try:
            # print(type(uuid.UUID(home_id)), type(home_id))
            criteria = QueryFilter(home=str(home_id))
            response = super().find_by_criteria(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)[0]
            resp_data['home'] = str(resp_data['home'])
            # print("[Device][Retrived] There is " + len(resp_data) + " Devices Found in home_id " + home_id)
        except IndexError:
            resp_data=[]
            print("[Device][Retrived] There is no device found in home_id",home_id)
        except Exception as error:
            print("[Device][Error] Something went wrong.", error)
            raise error
        return resp_data

    def deleteDevice(self, device_id):
        try:
            criteria = QueryFilter(id=device_id)
            ChannelsManagement().deleteChannel(device_id=device_id)
            super().delete(criteria)
            print("Successfully Deleting Device:", device_id)

        except Exception as err:
            print(err)

        return device_id

    def add_device_home(self, home_id, device_key): 
        try: 
            device = DevicesManagement().find_by_key(key=device_key)  
            device['home_id'] = home_id
            DevicesManagement().update_device(data=device)
        except Exception as err:
            print(err)

    def remove_device_home(self, device_key):
        try:
            device = DevicesManagement().find_by_key(key=device_key)  
            device['home_id'] = None
            DevicesManagement().update_device(data=device)
        except Exception as err:
            print(err)
    

class ChannelsManagement(Repository):
    
    """
    Handles CRUD Logic Functionalities for Channel
    """

    def __init__(self):
        
        module = Module(name="Channels",
                        model=Channels,
                        serializer=ChannelsSerializer)
        super().__init__(module=module)


    def find_by_device_id(self, device_id):
        criteria = []
        criteria = QueryFilter(device=device_id)
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

    def update_temp_by_id(self, id, status):
        try: 
            criteria = QueryFilter(device=id)
            response = self.find_by_criteria(criteria)
            instance = common.get_value(idf.INSTANCES, response)

            temp = status["temp"]
            hum = status["hum"]
            for idx, stat in enumerate(status):
                print("Data", status[stat])
                updated={
                    idf.STATUS: status[stat]
                }
                update_save = super().update(updated, instance[idx])

            print("update_save",instance)
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
    
    def find_by_id(self, id):
        criteria = QueryFilter(id=id)
        channel_resp = []
        response = super().find_by_criteria(criteria)
        channel_resp = common.get_value(idf.SERIALIZED, response)[0]
        return channel_resp
    
    def createTempChannel(self, device):
        i = 0
        try:
            temp_obj = {
                'name': 'temperature',
                'device': str(device.id),
                'room': '',
                'status': '0'
            }
            super().save(temp_obj)

            
            hum_obj = {
                'name': 'huminity',
                'device': str(device.id),
                'room': '',
                'status': '0'
            }
            super().save(hum_obj)

        except Exception as error:
            print("[Error]",error)
            raise error

    def createChannels(self, device, count):
        i = 0
        try:
            while i < count:
                i += 1
                saved_data = {
                    'name': 'channel '+str(i),
                    'device': str(device.id),
                    'room': '',
                    'status': '0'
                }
                super().save(saved_data)
        except Exception as error:
            print("[Error]",error)
            raise error
        

    def deleteChannel(self, device_id):
        try:
            criteria = QueryFilter(device=device_id)
            super().delete(criteria)
            print("Successfully Deleting Device Channel:", device_id)

        except Exception as err:
            print(err)

        return device_id
    

    def updateChannel(self, id, data):
        try:
            temp_data = {
                'name': data['name'],
                'room': data['room']
            }
            criteria = QueryFilter(id=id)
            response = self.find_by_criteria(criteria)
            instance = common.get_value(idf.INSTANCES, response)[0]
            update_save = super().update(temp_data, instance)
            
        except Exception as err:
            print(err)