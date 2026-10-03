from django.shortcuts import render
from bookings.models import Movie, Booking, Seat

# Create your views here.
def booking_history(request):
    # Retrieve all the bookings from the Booking table
    bookings = Booking.objects.all()
    # Pass the bookings to the template for access on the page
    return render(request, "bookings/booking_history.html", {"bookings": bookings})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "bookings/movie_list.html", {"movies": movies})
    
def seat_booking(request):
    seats = Seat.objects.all()
    return render(request, "bookings/seat_booking.html", {"seats": seats})