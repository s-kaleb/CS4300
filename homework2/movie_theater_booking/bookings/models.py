from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    release_date = models.DateField()
    duration_minutes = models.PositiveIntegerField()

class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    booking_status = models.BooleanField(default=False)

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    user = models.CharField(max_length=50)
    booking_date = models.DateField()