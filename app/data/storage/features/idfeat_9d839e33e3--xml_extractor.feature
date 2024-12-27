Feature: XML Extractor

Scenario: Extracting XML files successfully
    Given I am on Paylslip with my user payslip details displayed
    When I click on Extract to XML
    Then my file is successfully extracted with the correct data