import { Given, When, Then } from 'playwright-bdd';
import { expect } from '@playwright/test';
import selectors from './selectors.json';

Given('I am on the Swag Labs login page', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
});

When('I enter {string} into the {string} field', async ({ page }, value, field) => {
  const selector = selectors[field.toLowerCase().replace(' ', '_') + '_field'].value;
  await page.fill(selector, value);
});

When('I click the {string} button', async ({ page }, button) => {
  const selector = selectors[button.toLowerCase().replace(' ', '_') + '_button'].value;
  await page.click(selector);
});

Then('I should be redirected to the products page', async ({ page }) => {
  await expect(page).toHaveURL('https://www.saucedemo.com/inventory.html');
});

Then('I should see an error message {string}', async ({ page }, errorMessage) => {
  const errorSelector = selectors.error_message.value;
  await expect(page.locator(errorSelector)).toHaveText(errorMessage);
});