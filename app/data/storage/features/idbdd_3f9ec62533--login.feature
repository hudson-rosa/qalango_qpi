Feature: Login API


@idscn_3f9ec62533-1 @track-api @track-automated @track-critical-test @track-smoke-test @track-mobile @time-1m
Scenario: User logs in with valid credentials
    Given a user has valid login credentials
    When the user sends a POST request to "/login" with their username and password
    Then the API response status should be 200
    And the response body should contain a valid access token


@idscn_3f9ec62533-2 @track-api @track-automated @track-critical-test @track-smoke-test @track-mobile @time-2m
Scenario: User logs in with invalid credentials
    Given a user provides invalid login credentials
    When the user sends a POST request to "/login" with incorrect username and password
    Then the API response status should be 401
    And the response body should contain an error message "Invalid credentials"