

Feature: Aporo Communicates Order to GnamGnam
  Upon receiving a Client's Order, Aporo servers:
      (a) save the Order and the Client's authentication credentials
      (c) save and process the Driver info and PDF, and
      (d) communicate the results to GnamGnam.

  Scenario: Client uploads document

    Given Aporo receives the document for a New Order
    When  the document finishes uploading to Aporo
    Then  Aporo communicates the New Order to GnamGnam

