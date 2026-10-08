Feature: Booking a movie

Scenario: As a user I want to book an available seat for a movie
    Given I am logged in as testuser1
    And I am on the seat_booking page
    And there is an available seat
    When I choose a movie
    And I choose an available seat
    And I choose a date
    And I submit the form
    Then I am taken to my booking history
    And the booking is listed