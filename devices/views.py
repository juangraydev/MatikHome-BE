from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from devices.management import DevicesManagement, ChannelsManagement

from core.util.custom_exceptions import *

from core.util.common import *

class DeviceAPI(APIView):
    
    def get(self, request):
    
        device_management = DevicesManagement()
        device_resp = device_management.find_all()

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=device_resp,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)



class DeviceESPAPI(APIView):
    
    def get(self, request):
        key = self.request.query_params['key']
        device_management = DevicesManagement()
        channel_management = ChannelsManagement()
        device_resp = device_management.find_by_key(key)
        channel_resp = channel_management.find_by_id_esp(device_resp['id'])

        resp_details = create_response_details()
        resp_payload = create_response(
                                       resp_data=channel_resp,
                                       resp_details=resp_details)
        return Response(resp_payload, status=status.HTTP_200_OK)