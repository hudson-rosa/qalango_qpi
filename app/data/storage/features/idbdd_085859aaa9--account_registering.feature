Feature: Account Registering


@idscn_085859aaa9-1 @track-api @track-manual @track-critical-test @track-smoke-test @time-3m
Scenario: Successful account registration with valid inputs
    Given The user is on the registration page
    When The user enters all the mandatory fields
    And the user clicks the "Register" button
    Then the system should display a success message: "Registration completed successfully."
    And the user should be automatically redirected to the login page