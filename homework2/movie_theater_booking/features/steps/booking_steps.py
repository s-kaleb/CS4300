from behave import given, when, then
from django.contrib.auth import get_user_model
from django.urls import reverse
from bookings.models import Booking, Movie, Seat
from behave.api.pending_step import StepNotImplementedError

User = get_user_model()
PASSWORD = "pass12345"

###########################################
# Given: adapted from Claude Code
###########################################
@given(u'I am logged in as testuser1')
def step_impl(context):
    # create the user
    context.user = User.objects.create_user(username="testuser1", password=PASSWORD)
    # log in as testuser1
    logged_in = context.test.client.login(username="testuser1", password=PASSWORD)
    # passes if the login was successful
    assert logged_in, "Login failed"


@given(u'I am on the seat_booking page')
def step_impl(context):
    # navigate to the seat_booking page
    context.response = context.test.client.get(reverse("seat_booking"))
    # passes if the status code is 200
    assert context.response.status_code == 200, (
        f"Expected 200 but got {context.response.status_code}"
    )


@given(u'there is an available seat')
def step_impl(context):
    # create a new seat with booking status as false
    context.seat = Seat.objects.create(seat_number=1, booking_status=False)

###########################################
# When: adapted from Claude Code
###########################################
@when(u'I choose a movie')
# create the movie entity for the booking
def step_impl(context):
     context.movie = Movie.objects.create(
        title="Movie One",
        description="A test movie",
        release_date="2024-01-01",
        duration_minutes=100,
    )


@when(u'I choose an available seat')
def step_impl(context):
    # select the seat from the list of available seats returned by the query
    context.chosen_seat = Seat.objects.filter(booking_status=False).first()
    #passes if an available seat was found
    assert context.chosen_seat is not None, "No available seat found"


@when(u'I choose a date')
def step_impl(context):
    # Create a booking date
    context.booking_date = "2030-05-05"


@when(u'I submit the form')
def step_impl(context):
    # add the movie, seat, and booking date to the form and submit a Post request
    context.response = context.test.client.post(
        reverse("seat_booking"),
        {
            "movie": context.movie.id,
            "seat": context.chosen_seat.id,
            "booking_date": context.booking_date
        }
    )


###########################################
# Then: adapted from Claude Code
###########################################
@then(u'I am taken to my booking history')
def step_impl(context):
    # passes if the response is a redirect to the booking history page
    assert context.response.status_code == 302, (
        f"Expected a redirect (302) but got {context.response.status_code}"
    )
    # get the expected URL for the booking history page
    expected = reverse("booking_history")
    # passes if the url is same as expected
    assert context.response.url == expected, (
        f"Expected redirect to {expected} but got {context.response.url}"
    )


@then(u'the booking is listed')
def step_impl(context):
    # Get request for the booking history page
    response = context.test.client.get(reverse("booking_history"))
    # passes if the response is successful
    assert response.status_code == 200
    # get the list of bookings sent to the template by the view
    bookings = list(response.context["bookings"])
    # passes if the length of the bookings is as expected
    assert len(bookings) == 1, f"Expected 1 booking but found {len(bookings)}"
    # get the booking from the retrieved bookings
    booking = bookings[0]
    # passes if the booking has the right user
    assert booking.user == context.user
    # passes if the booking has the right movie
    assert booking.movie == context.movie
    # passes if the booking has the right seat
    assert booking.seat == context.chosen_seat