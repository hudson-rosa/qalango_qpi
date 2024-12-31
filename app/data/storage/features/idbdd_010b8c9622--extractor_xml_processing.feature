Feature: Extractor XML Processing


@idscn_010b8c9622-1 @cov-e2e @cov-automated @time-1m
Scenario: Extract data from XML file
	Given I have an XML file containing user data
	When I use the XML extractor tool to parse the file
	Then the extracted data should contain user names, email addresses, and phone numbers
	And the XML extractor should handle missing or malformed tags gracefully


@idscn_010b8c9622-2 @cov-usability @cov-manual @time-3m
@smoke-test
Scenario: Handle missing XML tags
    Given I have an XML file with missing phone number tags
    When I use the XML extractor tool to parse the file
    Then the extracted data should contain the available information (name, email)
    And the tool should log an error for the missing phone number tags
    And the missing phone numbers should be marked as "Not Available"


@idscn_010b8c9622-3 @cov-e2e @cov-manual @time-75m
Scenario Outline: Extract data from XML file based on provided configuration
	Given I have an XML file containing "<field1>", "<field2>", and "<field3>"
	When I use the XML extractor tool to parse the file
	Then the extracted data should contain "<field1>", "<field2>", and "<field3>"
	And the XML extractor should process the data without errors

	Examples:
	  | field1   | field2     | field3      |
	  | name     | email      | phone       |
	  | address  | city       | zip_code    |
	  | order_id | product_id | quantity    |