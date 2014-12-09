
Feature: Client Computer Authentication via a Contract
  Aporo uses a Contract as one means of authenticating a Client. Each time a Client installs an Aporo Printer Driver ("Driver"), the Driver generates a random, highly-unique ID ("UUID") that is saved
  on the Client's computer. The Client can authenticate the Driver
  by printing (with the Aporo Delivery Driver) a Contract approved
  by an Aporo manager. This method of authenticating a Client's
  computer involves:
      (a) a manager printing a Client Contract with an Aporo Printer Driver having administrative credentials,
      (b) Aporo servers processing the contents of the Contract
            and registering the Client, and
      (c) the Client printing the same Contract to Aporo from
            any computer the Client wishes to authenticate.

  Scenario: a manager prints a contract

    Given url post request is made by an authenticated source
    When  the source transmits a Client Contract
    Then  a Client is registered with the content of the Contract

  Scenario: a client prints a registered contract

    Given a url post request is made by a non-authenticated source
    When  the source transmits a Client Contract
    And   the Client Contract is registered
    Then  Aporo authenticates the UUID of the source