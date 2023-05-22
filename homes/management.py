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

        house_list[idf.OBJ_ROOMS] = rooms_list
       
        # get_rooms_list_by_house
        return house_list
    
    def add_house(self, name):
        saved={}
        try:
            save_data= {
                idf.OBJ_NAME: name
            }
            saved = super().save(data=save_data)
        except Exception as exception:
            raise exception
        return saved
    
    def find_all(self):
        resp_data = []
        try:
            resp_data = super().find_all()
        except Exception as error:
            print("[Error]")
        
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


class HomeUserAccessManagement(Repository):

    def __init__(self):
        
        module = Module(name="HomeUserAccess",
                        model=HomeUserAccess,
                        serializer=HomeUserSerializer)
        super().__init__(module=module)
    
    def get_user_house(self, userId):
        house_list = []
        criteria = QueryFilter(user_id=userId)
        response = super().find_by_criteria(criteria)
        user_home_access_list = common.get_value(idf.SERIALIZED, response)
        for house in user_home_access_list:
            print(house['home'])
            home_temp = HomesManagement().get_house_list_by_id(house['home'])
            house_list.append(home_temp) 
        return house_list


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
    
