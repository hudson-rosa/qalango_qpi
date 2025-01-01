Feature: Payments


@idscn_d91cffe7db-1 @cov-e2e @cov-automated @time-5m
Scenario: Successful Payment Transaction
Given I am a registered user with a valid payment method
And I have items in my shopping cart ready for checkout
When I initiate the payment process
And I provide valid payment details
Then the payment should be processed successfully
And I should receive a payment confirmation
And my order status should be updated to "Paid"


@idscn_d91cffe7db-2 @cov-exploratory @cov-manual @time-10m
Scenario Outline: Payment Failure Due to Invalid Details
Given I am on the payment page with my order total displayed
When I provide invalid payment details such as "<field>"
Then I should see an error message "<error_message>"
And the payment should not be processed

Examples:
| field	               | error_message                                   |
| expired card	       | "Your card is expired."                        |
| incorrect CVV       | "The CVV code is incorrect."              |
| insufficient funds.  | "Insufficient funds in your account."   |