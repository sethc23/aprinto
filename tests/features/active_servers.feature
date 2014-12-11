

Feature: Verify Online Presence
    .

Scenario Outline: Confirm All Servers and Webpages are live

    Given "<page_title>" is live and we access "<webpage>"
    Then  the page should start loading within "<response_time>" seconds
    And   the response message should be "OK" with response code "200"

    Examples: Servers & Webpages
        | page_title                | webpage                                   | response_time |
        | Aporo                     | http://printer.aporodelivery.com          | 5.0           |
        | GnamGnam Home Page        | http://www.gnamgnamapp.com/               | 5.0           |
        | GnamGnam Join Us Page     | http://www.gnamgnamapp.com/join/          | 5.0           |
        | GnamGnam Admin Page       | http://admin.gnamgnamapp.com/login        | 5.0           |

