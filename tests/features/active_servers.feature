

Feature: Verify all servers are active
    .

Scenario: Confirm Aporo server is live

    Given we request a page on the Aporo server
    Then  the response code should be "200"
    And   the response message should be "OK"
