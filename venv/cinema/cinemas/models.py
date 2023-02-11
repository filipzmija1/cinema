from django.db import models


class ScreeningRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    places = models.IntegerField()
    projector_availability = models.BooleanField()


class RoomReservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(ScreeningRoom, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)


class Meta:
    unique_together = ('date', 'room_id')
