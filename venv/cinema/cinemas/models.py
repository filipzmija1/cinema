from django.db import models


class ScreeningRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    places = models.IntegerField()
    projector_availability = models.BooleanField()
