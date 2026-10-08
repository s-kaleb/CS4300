
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

######################################################
# Views: Adapted from Claude Implementation
######################################################

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

######################################################
# INTEGRATION TESTS adapted from Claude Implementation
######################################################

# Setup for the API, signing in as testuser1
class APIBaseTestCase(BaseTestCase):
    def setUp(self):
        self.api = APIClient()
        self.api.force_authenticate(user=self.user1)
 
# tests for the movie view set
class MovieViewSetTests(APIBaseTestCase):
    # test if an unauthenticated user request is rejected
    def test_unauthenticated_rejected(self):
        # make an apiclient instance and send a Get request to API
        response = APIClient().get(reverse(API_MOVIES))
        # passes if the error code is 401 or 403
        self.assertIn(response.status_code, (401, 403))
    
    # test is an authenticated user can access the movies in the API
    def test_authenticated_list(self):
        # make a Get request to the API, signed in as testuser1
        response = self.api.get(reverse(API_MOVIES))
        # passes if the request was successful
        self.assertEqual(response.status_code, 200)
        # passes if the retrieved number of movies is correct
        self.assertEqual(response.data["count"], 2)  # paginated response
 

# tests for the bookingviewset 
class BookingViewSetTests(APIBaseTestCase):
    # test if an unauthenticated user request is rejected
    def test_unauthenticated_rejected(self):
        # make a new APIclient instance not logged in, and send a Get request to the API
        response = APIClient().get(reverse(API_BOOKINGS_LIST))
        #passes if the error code is 401 or 403
        self.assertIn(response.status_code, (401, 403))
 
    # test if authorized user can access their bookings
    def test_list_returns_only_own_bookings(self):
        # make a Get request to the API as testuser1
        response = self.api.get(reverse(API_BOOKINGS_LIST))
        # passes if the request was successful
        self.assertEqual(response.status_code, 200)
        # Gathers the ids from the bookings associated with testuser1
        ids = [b["id"] for b in response.data["results"]]
        # passes if the ids matches the expected booking id for testuser1
        self.assertEqual(ids, [self.booking1.id])
 
    # test if creating a booking sets the user and marks the seat as taken
    def test_create_sets_user_and_marks_seat_taken(self):
        #make a valid post request to create a new booking
        response = self.api.post(
            reverse(API_BOOKINGS_LIST),
            {
                "movie": self.movie1.id,
                "seat": self.seat_free1.id,
                "booking_date": "2030-05-05",
            },
            format="json",
        )
        #passes if the booking was created successfully
        self.assertEqual(response.status_code, 201)
        #get the new booking from the database
        booking = Booking.objects.get(id=response.data["id"])
        #passes if the new bookings user is testuser1
        self.assertEqual(booking.user, self.user1)
        #update the seat 
        self.seat_free1.refresh_from_db()
        #passes if the seat is now taken
        self.assertTrue(self.seat_free1.booking_status)
 
    # test if creating a booking with a taken seat returns 400 error
    def test_create_with_taken_seat_returns_400(self):
        # make a post request with a taken seat
        response = self.api.post(
            reverse(API_BOOKINGS_LIST),
            {
                "movie": self.movie1.id,
                "seat": self.seat_taken2.id,
                "booking_date": "2030-05-05",
            },
            format="json",
        )
        # passes if the error code 400 is returned
        self.assertEqual(response.status_code, 400)
        # passes if the booking wasn't created
        self.assertEqual(Booking.objects.count(), 2)
 
    # test if updating a booking to a new seat frees the old seat and takes the new one
    def test_update_to_new_seat_frees_old_and_takes_new(self):
        # Make a request to update the seat to seat_free1
        response = self.api.patch(
            reverse(API_BOOKING_DETAIL, args=[self.booking1.id]),
            {"seat": self.seat_free1.id},
            format="json",
        )
        # passes if the request was successful
        self.assertEqual(response.status_code, 200)
        # refresh to get updated booking_status
        self.seat_taken1.refresh_from_db()
        # refresh to get the updated booking_status
        self.seat_free1.refresh_from_db()
        # passes if the old seat is free
        self.assertFalse(self.seat_taken1.booking_status)
        # passes if the new seat is taken
        self.assertTrue(self.seat_free1.booking_status)
 
    # test if updating a booking while keeping the same seat leaves the seat taken
    def test_update_keeping_same_seat_leaves_seat_taken(self):
        # make a request to update the booking date while keeping seat the same
        response = self.api.patch(
            reverse(API_BOOKING_DETAIL, args=[self.booking1.id]),
            {"booking_date": "2031-01-01"},
            format="json",
        )
        # passes if the request was successful
        self.assertEqual(response.status_code, 200)
        # refresh the seat to get the updated booking_status
        self.seat_taken1.refresh_from_db()
        # passes if the seat is still taken
        self.assertTrue(self.seat_taken1.booking_status)
 
    # test if updating a booking to a taken seat returns 400 error
    def test_update_to_taken_seat_returns_400(self):
        # make a request to update the seat to a taken seat
        response = self.api.patch(
            reverse(API_BOOKING_DETAIL, args=[self.booking1.id]),
            {"seat": self.seat_taken2.id},
            format="json",
        )
        # passes if the request returns an error code 400
        self.assertEqual(response.status_code, 400)

    # test if deleting a booking updates the booking_status
    def test_delete_removes_booking_and_frees_seat(self):
        # make a request to delete the booking
        response = self.api.delete(
            reverse(API_BOOKING_DETAIL, args=[self.booking1.id])
        )
        # passes if the request was successful
        self.assertEqual(response.status_code, 204)
        # passes if the booking is deleted
        self.assertFalse(Booking.objects.filter(id=self.booking1.id).exists())
        # refresh the seat to get the updated booking_status
        self.seat_taken1.refresh_from_db()
        # passes if the seat is free
        self.assertFalse(self.seat_taken1.booking_status)
 
    # test if testuser1 can access testuser2's booking
    def test_cannot_access_other_users_booking(self):
        # get the path to the booking for testuser2
        url = reverse(API_BOOKING_DETAIL, args=[self.booking2.id])
        # passes if the request returns a 404 error
        self.assertEqual(self.api.get(url).status_code, 404)
        #passes if updating the booking fails and returns 404 error
        self.assertEqual(
            self.api.patch(url, {"seat": self.seat_free1.id}, format="json").status_code,
            404,
        )
        # passes if failts to delete the booking and returns 404 error
        self.assertEqual(self.api.delete(url).status_code, 404)
        # passes if the booking wasn't deleted from the database
        self.assertTrue(Booking.objects.filter(id=self.booking2.id).exists())
 
 # tests for the SeatViewSet
class SeatViewSetTests(APIBaseTestCase):
    
    # test if the unauthenticated user is unable to access the seats list
    def test_unauthenticated_rejected(self):
        # make a APIClient Get request for seat list
        response = APIClient().get(reverse(API_SEATS_LIST))
        # passes if an error code 401 or 403 is returned
        self.assertIn(response.status_code, (401, 403))
    
    # test if the authenticated user can access the seats list
    def test_authenticated_list(self):
        # make a get request for the seats list
        response = self.api.get(reverse(API_SEATS_LIST))
        # passes if the request was successful
        self.assertEqual(response.status_code, 200)
        # passes if the number of seats matches the expected number
        self.assertEqual(response.data["count"], 4)
 
    # test if updating a seat cannot change the booking status
    def test_update_cannot_change_booking_status(self):
        # make a patch request to update the seats booking status
        response = self.api.patch(
            reverse(API_SEAT_DETAIL, args=[self.seat_free1.id]),
            {"seat_number": 99, "booking_status": True},
            format="json",
        )
        # passes if the request was successful
        self.assertEqual(response.status_code, 200)
        # refresh the seat to get the updated booking_status
        self.seat_free1.refresh_from_db()
        # passes if the seat number was updated
        self.assertEqual(self.seat_free1.seat_number, 99)
        # passes if the booking status is still false
        self.assertFalse(self.seat_free1.booking_status)  