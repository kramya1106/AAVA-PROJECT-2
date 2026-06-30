"""
Page object for the user registration page.
This page contains all registration form elements and actions.
"""

from playwright.sync_api import Page
from pages.base_page_object import BasePageObject


class RegistrationPage(BasePageObject):
    """Page object for user registration page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.elements.registration_form = "form#registrationForm, form.registration-form, form:has(input[name='firstName']):has(input[name='email'])"
        self.elements.first_name_input = "input#firstName, input[name='firstName'], input[placeholder*='First Name']"
        self.elements.last_name_input = "input#lastName, input[name='lastName'], input[placeholder*='Last Name']"
        self.elements.email_input = "input#email, input[name='email'], input[type='email'], input[placeholder*='Email']"
        self.elements.password_input = "input#password, input[name='password'], input[type='password'][placeholder*='Password']:not([placeholder*='Confirm'])"
        self.elements.confirm_password_input = "input#confirmPassword, input[name='confirmPassword'], input[type='password'][placeholder*='Confirm']"
        self.elements.register_button = "button[type='submit'], button#registerBtn, button:has-text('Register'), button:has-text('Sign Up')"
        self.elements.loading_indicator = ".loading, .spinner, #loadingIndicator, [class*='loading'], [class*='spinner']"
    
    def navigate_to_registration_page(self, url: str):
        """Navigate to the registration page URL and wait for page to load."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle", timeout=30000)
        self.registration_form.wait_for(state="visible", timeout=30000)
    
    def enter_first_name(self, first_name: str):
        """Clear and enter first name in the first name input field."""
        self.first_name_input.wait_for(state="visible", timeout=5000)
        self.first_name_input.clear()
        self.first_name_input.fill(first_name)
    
    def enter_last_name(self, last_name: str):
        """Clear and enter last name in the last name input field."""
        self.last_name_input.wait_for(state="visible", timeout=5000)
        self.last_name_input.clear()
        self.last_name_input.fill(last_name)
    
    def enter_email(self, email: str):
        """Clear and enter email address in the email input field."""
        self.email_input.wait_for(state="visible", timeout=5000)
        self.email_input.clear()
        self.email_input.fill(email)
    
    def enter_password(self, password: str):
        """Clear and enter password in the password input field."""
        self.password_input.wait_for(state="visible", timeout=5000)
        self.password_input.clear()
        self.password_input.fill(password)
    
    def enter_confirm_password(self, confirm_password: str):
        """Clear and enter confirm password in the confirm password input field."""
        self.confirm_password_input.wait_for(state="visible", timeout=5000)
        self.confirm_password_input.clear()
        self.confirm_password_input.fill(confirm_password)
    
    def click_register_button(self):
        """Click the register button to submit the registration form."""
        self.register_button.wait_for(state="visible", timeout=5000)
        self.register_button.click()
    
    def wait_for_registration_complete(self, timeout: int = 30):
        """Wait for registration processing to complete by waiting for loading indicator to disappear."""
        if self.loading_indicator.is_visible():
            self.loading_indicator.wait_for(state="hidden", timeout=timeout * 1000)
    
    def is_registration_form_visible(self) -> bool:
        """Check if the registration form is visible on the page."""
        return self.registration_form.is_visible()
    
    def is_password_masked(self) -> bool:
        """Verify that the password field has type='password' attribute ensuring password is masked."""
        password_type = self.password_input.get_attribute("type")
        return password_type == "password"
    
    def is_confirm_password_masked(self) -> bool:
        """Verify that the confirm password field has type='password' attribute ensuring password is masked."""
        confirm_password_type = self.confirm_password_input.get_attribute("type")
        return confirm_password_type == "password"
    
    def fill_registration_form(self, first_name: str, last_name: str, email: str, password: str):
        """Fill all registration form fields with provided data."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_confirm_password(password)
    
    def submit_registration(self):
        """Submit the registration form and wait for processing."""
        self.click_register_button()
        self.wait_for_registration_complete()
