from bookings.models import Movie, Booking, Seat
from rest_framework import serializers

# Serializers for the booking system: from devedu AI
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ['user',]
    
    def validate(self, data):
        seat = data.get("seat")

        if seat is not None and seat.booking_status:
            raise serializers.ValidationError("This seat is already taken.")
        return data
        