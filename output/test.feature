```
Feature: Login to Swag Labs

  Background:
    Given I am on the Swag Labs login page

  Scenario: Successful login with standard user
    When I enter "standard_user" into the "Username" field
    And I enter "secret_sauce" into the "Password" field
    And I click the "Login" button
    Then I should be redirected to the products page

  Scenario: Login with locked out user
    When I enter "locked_out_user" into the "Username" field
    And I enter "secret_sauce" into the "Password" field
    And I click the "Login" button
    Then I should see an error message "Sorry, this user has been locked out."

  Scenario: Login with problem user
    When I enter "problem_user" into the "Username" field
    And I enter "secret_sauce" into the "Password" field
    And I click the "Login" button
    Then I should be redirected to the products page

  Scenario: Login with performance glitch user
    When I enter "performance_glitch_user" into the "Username" field
    And I enter "secret_sauce" into the "Password" field
    And I click the "Login" button
    Then I should be redirected to the products page
```
