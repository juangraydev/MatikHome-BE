import logging
import jwt
from core.repository.repository import Repository
from core.repository.repository import Module
from django.db.models import Q as QueryFilter, Value
from core.constants import identifer as idf
from homes.models import *
from homes.serializers import *
import json
from django.conf import settings
from core.util.custom_exceptions import *


from core.util import common
from core.auth.token_authentication import TokenAuthentication

class HomesManagement(Repository):
    """
    Handles CRUD Logic Functionalities for User
    """

    def __init__(self):
        
        module = Module(name="Home",
                        model=Homes,
                        serializer=HomesSerializer)
        super().__init__(module=module)

    def get_house_list_by_id(self, id):
        house_list = {}
        criteria = QueryFilter(id=id)
        response = super().find_by_criteria(criteria)
        house_list = common.get_value(idf.SERIALIZED, response)[0]
        rooms_list = RoomManagement().get_rooms_list_by_house(house_list[idf.OBJ_ID])
        member_list = HomeUserAccessManagement().get_home_members(house_list[idf.OBJ_ID])

        house_list[idf.OBJ_ROOMS] = rooms_list
        house_list[idf.OBJ_MEMBERS] = member_list
       
        # get_rooms_list_by_house
        return house_list
    
    def add_house(self, data):
        saved={}
        try:
            save_data= {    
                idf.OBJ_NAME: data['name'],
                idf.OBJ_ADDRESS: data['address']
            }
            saved = super().save(data=save_data)
            # RoomManagement().add_rooms_by_house()
            for room in data['rooms']:
                room_data = {
                    "home_id": saved.id,
                    "room": room
                }
                RoomManagement().add_rooms_by_house(data=room_data)
        except Exception as exception:
            raise exception
        return saved
    
    def edit_house(self, data):
        updated={}
        try:
            criteria = QueryFilter(id=data['id'])
            response = self.find_by_criteria(criteria)
            instance = common.get_value(idf.INSTANCES, response)[0]
            updated = self.update(data, instance)
            # response = super().save_or_update(data,criteria)
            # updated = common.get_value(idf.SERIALIZED, response)
        except Exception as exception:
            raise exception
        return updated
    
    def find_all(self):
        resp_data = []
        try:
            response = super().find_all()

            for home in response:
                resp_home = self.get_house_list_by_id(home[idf.OBJ_ID])
                resp_data.append(resp_home)
        except Exception as error:
            print("[Error][Home]: ${error}")
        
        return resp_data

class RoomManagement(Repository):

    def __init__(self):
        
        module = Module(name="Rooms",
                        model=Rooms,
                        serializer=RoomsSerializer)
        super().__init__(module=module)

    def get_rooms_list_by_house(self, id):
        rooms_list = []
        criteria = QueryFilter(home_id=id)
        response = super().find_by_criteria(criteria)
        rooms_instance = common.get_value(idf.SERIALIZED, response)

        for room in rooms_instance:
            roomTemp = {}
            roomTemp[idf.OBJ_ID] = room[idf.OBJ_ID]
            roomTemp[idf.NAME] = room[idf.NAME]
            roomTemp[idf.OBJ_TYPE] = room[idf.OBJ_TYPE]
            rooms_list.append(roomTemp)

        return rooms_list
    
    def add_rooms_by_house(self, data):
        resp_data = {}
        try:
            room={
                "home": data['home_id'],
                idf.NAME: data['room']['name'],
                idf.OBJ_TYPE: data['room']['type']
            }
            response = super().save(room)
            resp_data = common.get_value(idf.SERIALIZED, response)
        except Exception as exception:
            raise exception

        return resp_data
    
    def edit_room(self, data):
        
        criteria = QueryFilter(id=data['id'])

        response = super().save_or_update(data,criteria)
        rooms_instance = common.get_value(idf.SERIALIZED, response)
            
        return rooms_instance
    
    def delete_room(self, id):
        resp_data = {}
        try:
            criteria = QueryFilter(id=id)

            response = super().delete(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)
        except Exception as exception:
            raise RoomDeleteError
            
        return resp_data


class HomeUserAccessManagement(Repository):
    
    def __init__(self):
        
        module = Module(name="HomeUserAccess",
                        model=HomeUserAccess,
                        serializer=HomeUserSerializer)
        super().__init__(module=module)
    
    def get_user_house(self, userId):
        house_list = []
        try:
            criteria = QueryFilter(user=str(userId))
            response = super().find_by_criteria(criteria)
            user_home_access_list = common.get_value(idf.SERIALIZED, response)
            for house in user_home_access_list:
                home_temp = HomesManagement().get_house_list_by_id(house['home'])
                house_list.append(home_temp) 

        except Exception as err:
            print(err)
            raise err
        return house_list
    
    def get_home_members(self, homeId):
        from user.management import UserManagement 
        member_list = []
        user_mgnt = UserManagement()
        try: 
            
            criteria = QueryFilter(home=homeId)
            response = super().find_by_criteria(criteria)
            response = common.get_value(idf.SERIALIZED, response)

            for member_access in response:
                member = user_mgnt.find_by_id(member_access['user'])
                member_data = {
                    idf.OBJ_ID: member['id'],
                    'full_name': member['first_name'] + " " + member['last_name'],
                    'role': member_access['role']
                }
                member_list.append(member_data)
        
        except Exception as err:

            print(err)

        return member_list

    def add_user_house(self, userId, homeId):
        saved = {}
        try:
            save_data = {
                'user': userId,
                'home': homeId
            }
            saved = super().save(save_data)
        except Exception as exception:
            print("[Error]", exception)
            raise exception
        
        return saved
    
    def delete_user_access(self, userId): 
        try:
            criteria = QueryFilter(user=userId)
            response = super().delete(criteria)
            response = common.get_value(idf.SERIALIZED, response)
        except Exception as err:
            print("[User Access]", err)
