from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    release_date = models.DateField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Seat(models.Model):
    seat_number = models.PositiveIntegerField(unique=True)
    booking_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number}"

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateField()

    def __str__(self):
        return f"{self.movie.title} Seat {self.seat.seat_number}"