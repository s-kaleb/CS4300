
# access to the user model 
from django.contrib.auth import get_user_model
from django.test import TestCase
# get paths
from django.urls import reverse
# testing REST API
from rest_framework.test import APIClient
 
from bookings.models import Booking, Movie, Seat
 


User = get_user_model()
 
URL_LOGIN = "login"
URL_MOVIE_LIST = "movie_list"
URL_SEAT_BOOKING = "seat_booking"
URL_BOOKING_HISTORY = "booking_history"
API_MOVIES = "movie-list"
API_SEATS_LIST = "seat-list"
API_SEAT_DETAIL = "seat-detail"
API_BOOKINGS_LIST = "booking-list"
API_BOOKING_DETAIL = "booking-detail"



# Create your tests here.

# TODO: 80% code coverage

# Sets up the data used for testing: adapted from Claude Code
class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create users
        cls.user1 = User.objects.create_user(username="testuser1", password="pass12345")
        cls.user2 = User.objects.create_user(username="testuser2", password="pass12345")
    
        # create movies
        cls.movie1 = Movie.objects.create(
            title="Movie One",
            description="First movie",
            release_date="2024-01-01",
            duration_minutes=100,
        )
        cls.movie2 = Movie.objects.create(
            title="Movie Two",
            description="Second movie",
            release_date="2024-02-02",
            duration_minutes=120,
        )
 
        # Free seats
        cls.seat_free1 = Seat.objects.create(seat_number=100, booking_status=False)
        cls.seat_free2 = Seat.objects.create(seat_number=101, booking_status=False)

        # Seats already taken by the two users' bookings
        cls.seat_taken1 = Seat.objects.create(seat_number=102, booking_status=True)
        cls.seat_taken2 = Seat.objects.create(seat_number=103, booking_status=True)
 
        # Make bookings
        cls.booking1 = Booking.objects.create(
            movie=cls.movie1,
            seat=cls.seat_taken1,
            user=cls.user1,
            booking_date="2030-01-01",
        )
        cls.booking2 = Booking.objects.create(
            movie=cls.movie2,
            seat=cls.seat_taken2,
            user=cls.user2,
            booking_date="2030-01-02",
        )

#####################################
# Views: Claude Implementation
#####################################

# tests for booking_history view, and template.
class BookingHistoryViewTests(BaseTestCase):

    # Checks if redirect for logged out user
    # goes to the login page correctly
    def test_anonymous_redirected_to_login(self):
        # saving the path to booking history
        url = reverse(URL_BOOKING_HISTORY)
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse(URL_LOGIN)}?next={url}",
            fetch_redirect_response=False,
        )
 
    # checks if user1 can only see their own bookings
    def test_shows_only_current_users_bookings(self):
        #login the user
        self.client.login(username="testuser1", password="pass12345")
        #navigate to the page
        response = self.client.get(reverse(URL_BOOKING_HISTORY))
        # Check if page got rendered correct
        self.assertEqual(response.status_code, 200)
        # checks that the correct template was used
        self.assertTemplateUsed(response, "bookings/booking_history.html")
        # get the bookings passed to the template
        bookings = list(response.context["bookings"])
        # Checks if the bookings matches the booking for testuser1
        self.assertEqual(bookings, [self.booking1])
        # checks to make sure testuser2's booking is not in bookings
        self.assertNotIn(self.booking2, bookings)
 
 
# test the movie list view
class MovieListViewTests(BaseTestCase):

    # Test is the page is visible by anyone and contains all movies in db
    def test_movie_list_is_public_and_lists_all_movies(self):
        # get request for movie_list page
        response = self.client.get(reverse(URL_MOVIE_LIST))
        # passes if navigation was successful
        self.assertEqual(response.status_code, 200)
        # passes if correct template was used
        self.assertTemplateUsed(response, "bookings/movie_list.html")
        # passes if contains all movies
        self.assertCountEqual(
            response.context["movies"], [self.movie1, self.movie2]
        )
 
# tests for the seat_booking view
class SeatBookingViewTests(BaseTestCase):

    # Get the path to the view and login to the test user
    def setUp(self):
        self.url = reverse(URL_SEAT_BOOKING)
        self.client.login(username="testuser1", password="pass12345")
    
    # test if not signed in user is redirected to the login page
    def test_anonymous_redirected_to_login(self):
        # log out of the test account
        self.client.logout()
        # send Get request fot seat_booking page
        response = self.client.get(self.url)
        # Check if the redirect is to the correct page
        self.assertRedirects(
            response,
            f"{reverse(URL_LOGIN)}?next={self.url}",
            fetch_redirect_response=False,
        )
 
    # Tests if the seat_booking has the right number of data passed
    # also tests if get request is correct and no errors occured.
    def test_get_renders_form_with_seats_and_movies(self):
        # Sends a get request for the seat_booking page
        response = self.client.get(self.url)
        # Passes if get request was successful
        self.assertEqual(response.status_code, 200)
        # passes if the correct template was used
        self.assertTemplateUsed(response, "bookings/seat_booking.html")
        # passes if there are four seat options
        # Gets the seats passed to the template from the view and compares
        self.assertEqual(response.context["seats"].count(), 4)
        # passes if the number of movies passed to the template from the view is correct
        self.assertEqual(response.context["movies"].count(), 2)
        # passes if no errors appeared
        self.assertNotIn("error", response.context)
 
    # Tests proper handling if user doesn't submit correct form
    def test_post_missing_fields_returns_400(self):
        # the data of a correct form
        base = {
            "movie": self.movie1.id,
            "seat": self.seat_free1.id,
            "booking_date": "2030-05-05",
        }

        # each loop leaves out a different field from base
        for missing in base:
            # each loop is a test
            with self.subTest(missing=missing):
                # data = base - missing
                data = {k: v for k, v in base.items() if k != missing}
                # post request with incomplete data
                response = self.client.post(self.url, data)
                # passes if got the correct error code
                self.assertEqual(response.status_code, 400)
                # passes if the error text matches
                self.assertIn("Have to enter a value for all fields.", response.context["error"])
        # Passes if no new bookings were created
        self.assertEqual(Booking.objects.count(), 2)
 
    # tests behavior if nonexistent movie is entered
    def test_post_nonexistent_movie_returns_400(self):
        # post request for a movie that doesn't exist
        response = self.client.post(
            self.url,
            {"movie": 9999, "seat": self.seat_free1.id, "booking_date": "2030-05-05"},
        )
        # Passes if error code 400 
        self.assertEqual(response.status_code, 400)
        # Passes if error message is shown
        self.assertIn("The Movie or Seat entered does not exist.", response.context["error"])
 
    # tests behavior if nonexistent seat is entered
    def test_post_nonexistent_seat_returns_400(self):
        # Post request for a non existant seat
        response = self.client.post(
            self.url,
            {"movie": self.movie1.id, "seat": 9999, "booking_date": "2030-05-05"},
        )
        # passes if error code 400 is made
        self.assertEqual(response.status_code, 400)
        # passes if error message matches
        self.assertIn("The Movie or Seat entered does not exist.", response.context["error"])
 
    # test for entering chars instead of int for id
    def test_post_non_integer_id_returns_400(self):
        # post request for a booking with movie id as abc
        response = self.client.post(
            self.url,
            {"movie": "abc", "seat": self.seat_free1.id, "booking_date": "2030-05-05"},
        )
        # passes if error code 400
        self.assertEqual(response.status_code, 400)
        # passes if error message matches
        self.assertIn("The Movie or Seat entered does not exist.", response.context["error"])
 
    # Test for taken seat passed to booking form
    def test_post_taken_seat_returns_400_and_creates_nothing(self):
        # post request containing a taken seat
        response = self.client.post(
            self.url,
            {
                "movie": self.movie1.id,
                "seat": self.seat_taken2.id,
                "booking_date": "2030-05-05",
            },
        )
        # passes if the error code matches 400
        self.assertEqual(response.status_code, 400)
        # passes if error message matches
        self.assertIn("That seat is already taken.", response.context["error"])
        # passes if no new booking is created
        self.assertEqual(Booking.objects.count(), 2)
 
    # test valid creation of a booking
    def test_post_valid_creates_booking_marks_seat_and_redirects(self):
        # post request containing valid data
        response = self.client.post(
            self.url,
            {
                "movie": self.movie1.id,
                "seat": self.seat_free1.id,
                "booking_date": "2030-05-05",
            },
        )
        # passes if after submission you are redirected to the booking_history page
        self.assertRedirects(
            response, reverse(URL_BOOKING_HISTORY), fetch_redirect_response=False
        )
        # gets the new booking by looking for the seat
        booking = Booking.objects.get(seat=self.seat_free1)
        # passes if the user is correct
        self.assertEqual(booking.user, self.user1)
        # passes if the movie is correct
        self.assertEqual(booking.movie, self.movie1)
        # update the value of the seat
        self.seat_free1.refresh_from_db()
        # pass if the seat is booked
        self.assertTrue(self.seat_free1.booking_status)


# Models


# Accounts



# INTEGRATION TESTS
