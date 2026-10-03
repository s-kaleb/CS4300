from django.shortcuts import render

# Create your views here.
def booking_history(request):
    return render(request, "bookings/booking_history.html")

def movie_list(request):
    return render(request, "bookings/movie_list.html")
    
def seat_booking(request):
    return render(request, "bookings/seat_booking.html")