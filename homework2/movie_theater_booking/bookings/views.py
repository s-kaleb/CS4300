from django.shortcuts import render, redirect
from bookings.models import Movie, Booking, Seat
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def booking_history(request):
    # Retrieve all the bookings from the Booking table that match the current user
    bookings = Booking.objects.filter(user=request.user)
    # Pass the bookings to the template for access on the page
    return render(request, "bookings/booking_history.html", {"bookings": bookings})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "bookings/movie_list.html", {"movies": movies})
    
"""def seat_booking(request):
    seats = Seat.objects.all()
    movies = Movie.objects.all()
    return render(request, "bookings/seat_booking.html", {"seats": seats, "movies": movies})
"""

# GPT seat_booking field with changes to match my needs
@login_required
def seat_booking(request):
    seats = Seat.objects.all()
    movies = Movie.objects.all()

    # If the user has created a booking and presses the submit button
    # we need to update the database with that new entry
    if request.method == "POST":
        movie_id = request.POST["movie"]
        seat_id = request.POST["seat"]
        booking_date = request.POST["booking_date"]

        movie = Movie.objects.get(id=movie_id)
        seat = Seat.objects.get(id=seat_id)

        Booking.objects.create(
            movie=movie,
            seat=seat,
            user=request.user,
            booking_date=booking_date
        )
        # Need to update the seat to show as taken
        seat.booking_status = True
        seat.save()

        #go to the booking history page to see booking
        return redirect("booking_history")

    return render(
        request,
        "bookings/seat_booking.html",
        {
            "seats": seats,
            "movies": movies,
        }
    )


""" 
The following views are for the REST API
"""
#Copied from https://www.django-rest-framework.org/tutorial/quickstart/#serializers
# changed to match the booking system models and serializers using Devedu AI
from rest_framework import permissions, viewsets
from bookings.serializers import MovieSerializer, BookingSerializer, SeatSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class SeatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seats to be viewed or edited.
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]