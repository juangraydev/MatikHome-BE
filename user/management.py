import logging
import jwt
from core.repository.repository import Repository
from core.repository.repository import Module
from django.db.models import Q as QueryFilter, Value
from core.constants import identifer as idf
from user.models import *
from user.serializers import *
import json
from django.conf import settings
from core.util.custom_exceptions import *


from core.util import common
from core.auth.token_authentication import TokenAuthentication

class UserManagement(Repository):
    """
    Handles CRUD Logic Functionalities for User
    """

    def __init__(self):
        
        module = Module(name="User",
                        model=User,
                        serializer=UserSerializer)
        super().__init__(module=module)

    def find_by_username(self, username):
        try:
            criteria = QueryFilter(username=username)
            response = super().find_by_criteria(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)[0]
        except Exception as error:
            print("[Error] Username not Found", error)
            raise HTTP401Error

        return resp_data
    
    def find_by_id(self, user_id):
        try:
            criteria = QueryFilter(id=user_id)
            response = super().find_by_criteria(criteria)
            resp_data = common.get_value(idf.SERIALIZED, response)[0]
        except Exception as error:
            print("[Error] Username not Found", error)
            raise HTTP401Error

        return resp_data
    
    def find_all(self):
        resp_data = []
        try:
            resp_data = super().find_all()
            for row in resp_data:
                row[idf.NAME] = row[idf.OBJ_FIRST_NAME] + " " + row[idf.OBJ_LAST_NAME]
        except Exception as error:
            print("[ERROR][USERS] ${error}")
           
        return resp_data
    
    def find_by_home_id(self):

        return []
    
    def add_user(self):
        resp_data = []
        try:
            resp_data = super().find_all()
        except Exception as error:
            print("[Error]")
           
        return resp_data

    def login(self, request):
        resp_data={}
        token_auth = TokenAuthentication()
        try:
            user = self.find_by_username(request[idf.OBJ_USERNAME])
            req_pass = jwt.decode(request[idf.OBJ_PASSWORD].encode('UTF-8'), settings.SECRET_KEY)
            decrypted_pass = jwt.decode(user[idf.OBJ_PASSWORD].encode('UTF-8'), settings.SECRET_KEY)
            if(not decrypted_pass[idf.OBJ_PASSWORD] == req_pass[idf.OBJ_PASSWORD]):
                raise HTTP401Error
            resp_data[idf.TOKEN] = token_auth.encode_token(user)
        except Exception as error:
            print("[Error]", error)
            raise HTTP401Error

        return resp_data

    def register(self, request):
        resp_data={}
        data_obj = {
            idf.OBJ_ID: "",
            idf.OBJ_FIRST_NAME: request[idf.OBJ_FIRST_NAME],
            idf.OBJ_LAST_NAME: request[idf.OBJ_LAST_NAME],
            idf.OBJ_USERNAME: request[idf.OBJ_USERNAME],
            idf.OBJ_PASSWORD: request[idf.OBJ_PASSWORD],
            idf.ROLE: 0,
        }
        token_auth = TokenAuthentication()
        try:
            user_saved = super().save(data_obj)
            resp_data = self.login(request=request)
            
        except Exception as error:
            print("[Error]", error)
            raise HTTP401Error 
        return resp_data
    
    
