 Feature: Saferpay

@e2e
Scenario: Paying with Saferpay
    Given the user is on the payment page
    And a product was added to the chart 
    When the user clicks on Pay button
    Then the product is successfully paid
                                        