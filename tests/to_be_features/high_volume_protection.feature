

Feature: Aporo Utilizes Other Servers When Experiencing Heavy Volume

  Scenario: Aprinto is not experiencing heavy volume

    Given Client communicates handshake
    When  Client prints with the Driver
    Then  Aprinto should reply with a Url for the Driver to send the print job
    And   Receive the print

  Scenario: Aprinto is experiencing too much volume

    Given Client communicates handshake at the URL
    When  Client prints with the Driver
    Then  Aprinto will not respond to the Client's handshake request

  Scenario: Aprinto is experiencing heavy volume

    Given Client communicates handshake at the URL
    When  Client prints with the Driver
    Then  Aprinto should identify an alternative destination for the Client's order
    And   Aprinto should provide said destination in response to the Client's handshake request
