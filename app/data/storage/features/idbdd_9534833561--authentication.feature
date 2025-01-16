Feature: Login


@idscn_9534833561-1 @track-e2e @track-manual @track-critical-test @track-desktop @track-mobile @track-smoke-test @time-3m
Scenario: User logs in and accesses the dashboard
    Given the user is on the login page
    When the user enters valid credentials
    And clicks the "Login" button
    Then the user should be redirected to the dashboard
    And the dashboard should display a welcome message


@idscn_9534833561-2 @track-e2e @track-automated @track-critical-test @track-edge-case @track-smoke-test @track-mobile @track-desktop @time-1m
Scenario: User tries to log in without providing credentials
    Given the user is on the login page
    When the user clicks the "Login" button without entering username or password
    Then an error message "Username and password are required" should be displayed


@idscn_9534833561-3 @track-integration @track-automated @track-critical-test @track-smoke-test @track-desktop @track-mobile @time-1m
Scenario: Valid user login and token verification
    Given a user sends a POST request to "/login" with valid credentials
    When the login API generates an access token
    And the token is verified by the token validation service
    Then the response should confirm the token is valid
    And the user should be marked as authenticated


@idscn_9534833561-4 @track-integration @track-automated @track-critical-test @track-edge-case @track-mobile @time-1m
Scenario: Login fails due to authentication service unavailability
    Given a user sends a POST request to "/login" with valid credentials
    When the authentication service is down
    Then the API response status should be 500
    And the response body should contain an error message "Authentication service unavailable"