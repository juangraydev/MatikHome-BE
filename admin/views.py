from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from homes.management import *
from admin.management import *

from core.util.custom_exceptions import *

from core.util.common import *

class UserListAPI(APIView):
    def get(self, request):
        user_management = UserManagement()
        user_list = user_management.find_all()
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=user_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    


class HomeListAPI(APIView):
    def get(self, request):
        admin_management = AdminManagement()
        home_list = admin_management.get_home_list()
        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=home_list,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)
    

