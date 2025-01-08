Feature: Extractor XML Processing


@idscn_2354d7e676-1 @track-e2e @track-manual @track-critical-test @track-smoke-test @track-desktop @time-15m
Scenario: Extract data from XML file
	Given I have an XML file containing user data
	When I use the XML extractor tool to parse the file
	Then the extracted data should contain user names, email addresses, and phone numbers
	And the XML extractor should handle missing or malformed tags gracefully


@idscn_2354d7e676-2 @track-contract @track-automated @track-mobile @track-edge-case @time-2m
Scenario: Handle missing XML tags
    Given I have an XML file with missing phone number tags
    When I use the XML extractor tool to parse the file
    Then the extracted data should contain the available information (name, email)
    And the tool should log an error for the missing phone number tags
    And the missing phone numbers should be marked as "Not Available"


@idscn_2354d7e676-3 @track-e2e @track-manual @track-desktop @track-mobile @track-smoke-test @time-15m
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