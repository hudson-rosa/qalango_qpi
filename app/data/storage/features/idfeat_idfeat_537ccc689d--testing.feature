# Example - BDD scenario
    Feature: User Login

  @usability
    Scenario: Successful login
        Given the user is on the login page
        When they enter valid credentials
        Then they should be redirected to the dashboard
                                        
    @e2e
    Scenario: Successful login
        Given the user is on the login page
        When they enter valid credentials
        Then they should be redirected to the dashboard