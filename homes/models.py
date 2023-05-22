from django.db import models
from user.models import User
from core.util.model_to_dict import ModelToDictionary

# Create your models here.

class Homes(models.Model, ModelToDictionary):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'Homes'
            

    def __str__(self):
        return self.id
    
class Rooms(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    home = models.ForeignKey(Homes, models.DO_NOTHING)
    type = models.IntegerField() ## 0 - Kitchen, 1 - Living Room, 2 - Garage, 3 - Bed Room, 5 - Office

    class Meta:
        managed = True
        db_table = 'Rooms'
            

    def __str__(self):
        return self.id

# Create your models here.

class HomeUserAccess(models.Model, ModelToDictionary):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    home = models.ForeignKey(Homes, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'HomeUserAccess'

    def __str__(self):
        return self.id