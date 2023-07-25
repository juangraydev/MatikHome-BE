from django.db import models
from homes.models import Homes
from homes.models import Rooms
import uuid
from django.utils.translation import gettext_lazy as _
from core.util.model_to_dict import ModelToDictionary
# Create your models here.

class Devices(models.Model, ModelToDictionary):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.UUIDField(default=uuid.uuid4, unique=True, null=False)
    home = models.ForeignKey(Homes, models.DO_NOTHING, null=True)

    class Meta:
        managed = True
        db_table = 'devices'
            

    def __str__(self):
        return self.id
    
class Channels(models.Model, ModelToDictionary):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    device = models.ForeignKey(Devices, models.DO_NOTHING)
    room = models.ForeignKey(Rooms, models.DO_NOTHING, null=True)
    status = models.CharField(max_length=1024, null=True)

    class Meta:
        managed = True
        db_table = 'channels'
            

    def __str__(self):
        return self.status