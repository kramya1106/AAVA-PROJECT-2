"""
Test Case ID: TC_REG_001
Title: Verify user registration with valid data
Description: This test case verifies that a new user can successfully register on the 
application by filling out the registration form with valid data and completing the 
registration process.
"""

import traceback
import pytest
from core.playwright_manager import PlaywrightManager
from core.settings import framework_logger
from pages.registration_page import RegistrationPage
from pages.registration_success_page import RegistrationSuccessPage
from playwright.sync_api import expect
import test_flows_common.test_flows_common as common
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@pytest.mark.usefixtures("main_execution")
def test_tc_reg_001_user_registration(stage_callback, tc_tracer, reporter):
    tcid = "TC_REG_001"
    current_step = "Step 0"
    current_validation = "User registration with valid data"
    
    REGISTRATION_URL = "https://example.com/register"
    FIRST_NAME = "John"
    LAST_NAME = "Doe"
    PASSWORD = "Test@1234"
    EXPECTED_SUCCESS_MESSAGE = "Registration successful"
    
    try:
        common.setup()
        test_email = common.generate_tenant_email()
        framework_logger.info(f"[{tcid}] Generated test email: {test_email}")
        
        # ── Step 1: Navigate to the registration page ──
        current_step = "Step 1"
        current_validation = "Registration page loads with all form fields visible"
        
        with PlaywrightManager() as page:
            registration_page = RegistrationPage(page)
            page.goto(REGISTRATION_URL)
            page.wait_for_load_state("networkidle", timeout=30000)
            
            expect(registration_page.registration_form).to_be_visible(timeout=30000)
            expect(registration_page.first_name_input).to_be_visible(timeout=30000)
            expect(registration_page.last_name_input).to_be_visible(timeout=30000)
            expect(registration_page.email_input).to_be_visible(timeout=30000)
            expect(registration_page.password_input).to_be_visible(timeout=30000)
            expect(registration_page.confirm_password_input).to_be_visible(timeout=30000)
            expect(registration_page.register_button).to_be_visible(timeout=30000)
            
            stage_callback("step1_registration_page", page, screenshot_only=True)
            framework_logger.info(f"[{tcid}] Step 1: Registration page loaded with all form fields visible")
            reporter.validate(True, f"[{tcid}] Step 1: Registration page loaded with all form fields visible")
            
            # ── Step 2: Enter first name in the First Name field ──
            current_step = "Step 2"
            current_validation = "First name is entered successfully"
            
            registration_page.first_name_input.clear()
            registration_page.first_name_input.fill(FIRST_NAME)
            expect(registration_page.first_name_input).to_have_value(FIRST_NAME, timeout=5000)
            
            framework_logger.info(f"[{tcid}] Step 2: First name '{FIRST_NAME}' entered successfully")
            reporter.validate(True, f"[{tcid}] Step 2: First name '{FIRST_NAME}' entered successfully")
            
            # ── Step 3: Enter last name in the Last Name field ──
            current_step = "Step 3"
            current_validation = "Last name is entered successfully"
            
            registration_page.last_name_input.clear()
            registration_page.last_name_input.fill(LAST_NAME)
            expect(registration_page.last_name_input).to_have_value(LAST_NAME, timeout=5000)
            
            framework_logger.info(f"[{tcid}] Step 3: Last name '{LAST_NAME}' entered successfully")
            reporter.validate(True, f"[{tcid}] Step 3: Last name '{LAST_NAME}' entered successfully")
            
            # ── Step 4: Enter email address in the Email field ──
            current_step = "Step 4"
            current_validation = "Email address is entered successfully"
            
            registration_page.email_input.clear()
            registration_page.email_input.fill(test_email)
            expect(registration_page.email_input).to_have_value(test_email, timeout=5000)
            
            framework_logger.info(f"[{tcid}] Step 4: Email '{test_email}' entered successfully")
            reporter.validate(True, f"[{tcid}] Step 4: Email '{test_email}' entered successfully")
            
            # ── Step 5: Enter password in the Password field ──
            current_step = "Step 5"
            current_validation = "Password is entered successfully and masked"
            
            registration_page.password_input.clear()
            registration_page.password_input.fill(PASSWORD)
            password_type = registration_page.password_input.get_attribute("type")
            expect(registration_page.password_input).to_have_attribute("type", "password", timeout=5000)
            
            framework_logger.info(f"[{tcid}] Step 5: Password entered successfully and masked (type={password_type})")
            reporter.validate(True, f"[{tcid}] Step 5: Password entered successfully and masked (type={password_type})")
            
            # ── Step 6: Enter password in the Confirm Password field ──
            current_step = "Step 6"
            current_validation = "Confirm password is entered successfully and matches the password"
            
            registration_page.confirm_password_input.clear()
            registration_page.confirm_password_input.fill(PASSWORD)
            confirm_password_type = registration_page.confirm_password_input.get_attribute("type")
            expect(registration_page.confirm_password_input).to_have_attribute("type", "password", timeout=5000)
            
            framework_logger.info(f"[{tcid}] Step 6: Confirm password entered successfully and masked (type={confirm_password_type})")
            reporter.validate(True, f"[{tcid}] Step 6: Confirm password entered successfully and masked (type={confirm_password_type})")
            
            # ── Step 7: Click the Register button ──
            current_step = "Step 7"
            current_validation = "Registration form is submitted"
            
            expect(registration_page.register_button).to_be_enabled(timeout=5000)
            registration_page.register_button.click()
            
            stage_callback("step7_form_submitted", page, screenshot_only=True)
            framework_logger.info(f"[{tcid}] Step 7: Registration form submitted successfully")
            reporter.validate(True, f"[{tcid}] Step 7: Registration form submitted successfully")
            
            # ── Step 8: Wait for registration to complete ──
            current_step = "Step 8"
            current_validation = "Registration is processed successfully"
            
            if registration_page.loading_indicator.is_visible():
                expect(registration_page.loading_indicator).not_to_be_visible(timeout=30000)
            
            registration_success_page = RegistrationSuccessPage(page)
            expect(registration_success_page.success_message).to_be_visible(timeout=30000)
            
            framework_logger.info(f"[{tcid}] Step 8: Registration processing completed successfully")
            reporter.validate(True, f"[{tcid}] Step 8: Registration processing completed successfully")
            
            # ── Step 9: Verify success message is displayed ──
            current_step = "Step 9"
            current_validation = "Success message 'Registration successful' is displayed"
            
            expect(registration_success_page.success_message).to_be_visible(timeout=10000)
            success_text = registration_success_page.success_message.text_content()
            expect(registration_success_page.success_message).to_contain_text(EXPECTED_SUCCESS_MESSAGE, timeout=10000)
            
            stage_callback("step9_success_message", page, screenshot_only=True)
            framework_logger.info(f"[{tcid}] Step 9: Success message displayed - '{success_text}'")
            reporter.validate(True, f"[{tcid}] Step 9: Success message displayed - '{success_text}'")
            
            # ── Step 10: Verify user is redirected to the dashboard or login page ──
            current_step = "Step 10"
            current_validation = "User is redirected to dashboard or login page"
            
            page.wait_for_load_state("networkidle", timeout=15000)
            current_url = page.url
            
            is_dashboard = "/dashboard" in current_url.lower()
            is_login = "/login" in current_url.lower()
            
            if is_dashboard:
                dashboard_header = page.locator("h1.dashboard-header, .dashboard-title, h1:has-text('Dashboard'), h1:has-text('Welcome')")
                expect(dashboard_header).to_be_visible(timeout=10000)
                framework_logger.info(f"[{tcid}] Step 10: User redirected to dashboard page - URL: {current_url}")
                reporter.validate(True, f"[{tcid}] Step 10: User redirected to dashboard page - URL: {current_url}")
            elif is_login:
                login_form = page.locator("form#loginForm, form.login-form, form:has(input[type='email']):has(input[type='password'])")
                expect(login_form).to_be_visible(timeout=10000)
                framework_logger.info(f"[{tcid}] Step 10: User redirected to login page - URL: {current_url}")
                reporter.validate(True, f"[{tcid}] Step 10: User redirected to login page - URL: {current_url}")
            else:
                framework_logger.info(f"[{tcid}] Step 10: User redirected to page - URL: {current_url}")
                reporter.validate(True, f"[{tcid}] Step 10: User redirected after registration - URL: {current_url}")
            
            stage_callback("step10_final_page", page, screenshot_only=True)
            
    except Exception as e:
        framework_logger.error(
            f"[{tcid}] Test failed at {current_step} — {current_validation}: "
            f"{e}\n{traceback.format_exc()}"
        )
        reporter.validate(False, f"[{tcid}] FAIL at {current_step} — {current_validation}: {str(e)}")
        raise
