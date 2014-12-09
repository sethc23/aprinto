

Feature: Client Communicates Order to Aporo
    Each time a Client prints an Order with an authenticated
    Aporo Printer Driver ("Driver"), the Driver, in a matter of milliseconds:
        (a) submits authentication credentials to Aporo,
        (b) receives an Order Tag and destination URL for submitting the Order,
        (c) transmits the Order to the destination URL, and
        (d) prints out the Order with the Order Tag at the local printer
                designated by the Client.
    .

    Scenario: Valid post to Aporo

        Given data for posting to Aporo
        When  the data is valid
        And   the data is posted to Aporo
        Then  Aporo creates a New Order
        And   Aporo returns an Order Tag, a Post Url, and QR code information

#  Scenario: Aporo receives a url post requests
#      Given the request includes a "machine_id" key
#      When  a Vendor has  is equal to "vendor"
#      Then Aporo creates a New Order
#      #creates a new order for <machine_id>
#      And Aporo returns an Order Tag
#      And Aporo returns a destination URL

#  Scenario: an non-authenticated client submits a handshake request
#      Given the machine_id does not have authentication_type vendor
#      Then  Aporo does not create a New Order
#      And   Aporo does not returns an Order Tag or destination URL

#  Scenario Outline: url post requests to shake hands
#    Given Aporo receives a handshake request with a <machine_id>
#    When  a <machine_id> has <authentication_type> equal to vendor
#    Then  Aporo creates a New Order
#    And   Aporo returns an Order Tag and destination URL
#
#    Examples: Requests
#        | machine_id      |   authentication_type   |
#        | vendor1         |   vendor                |
#        | admin1          |   manager               |
#        | random1         |   unknown               |


#  Scenario: an authenticated client submits a new order
#
#    Given an authenticated source
#    When  Aporo receives the authentication credentials
#    Then  Aporo creates a New Order
#    And   Aporo returns an Order Tag and destination URL
#
#  Scenario: an non-authenticated client submits a new order
#
#    Given url post request is made by an non-authenticated source
#    When  Aporo receives what looks like an order
#    Then  Aporo emails me immediately

# Planned/Upcoming Features:
#   -content authentication to minimize/eliminate a Client's non-order transmission
#   -immediate communication via email for any/all non-order transmissions and enclose PDF
#   -pop-up/audio client notification for new order from non-authenticated driver

#Feature: Zero-Downtime Configuration
  #Redirect Driver to secondary and tertiary servers for processing
