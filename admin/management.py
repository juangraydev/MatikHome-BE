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

from homes.management import HomesManagement 

from core.util import common
from core.auth.token_authentication import TokenAuthentication


class AdminManagement(Repository):
    """
    Handles CRUD Logic Functionalities for User
    """
    def __init__(self):

        super().__init__(module=[])

    def get_home_list(self):
        resp_data = []
        
        homes_management = HomesManagement()
        resp_data = homes_management.find_all()
        
        return resp_data
