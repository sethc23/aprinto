

Feature: Denial-of-Service Attack Prevention
  In order to minimize exposure to Denial-of-Service attacks,
  Aporo Delivery limits the number of URL post requests it processes
  from non-authenticated sources before blacklisting an IP address.

  Scenario: More than 5 url post requests from a non-authenticated source

    Given a url post request came from a non-authenticated source
    When  a non-authenticated source makes more than 5 url post requests
    Then  the IP of the source is added to the blacklist
    And   all further requests are immediately refused

  Scenario: More than 2 url post requests from a non-authenticated source
  with at least 1 improperly formed request

    Given a url post request came from a non-authenticated source
    When  a non-authenticated source makes an improperly formed url post request
    And   the non-authenticated source makes at least two other url post requests
    Then  the IP of the source is added to the blacklist
    And   all further requests are immediately refused
