Feature: Account Registration


@idscn_a5346199b8-1 @cov-usability @cov-manual @cov-critical-test @cov-edge-case @time-4m
Scenario: Successful account registration with valid inputs
Given The user is on the registration page
When The user enters all the mandatory fields
And the user clicks the "Register" button
Then the system should display a success message: "Registration completed successfully."
And the user should be automatically redirected to the login page