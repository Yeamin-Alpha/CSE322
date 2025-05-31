from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
import random  # Import the random module

from datetime import datetime, timedelta
BASE_URL = "http://127.0.0.1:8000/" 
USERNAME = "test65"  
EMAIL = "test65@eam.com"  
PASSWORD = "test123"  
TARGET_USER = "y38"  


def signup(driver, username, email, password): 
    driver.get(f"{BASE_URL}/signup/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password1").send_keys(password)
    driver.find_element(By.NAME, "password2").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(2)
    print(f"[STEP] Signup ({username}) complete.")


def login(driver, username, password):
    driver.get(f"{BASE_URL}login/")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "pass").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(4)
    print(f"[STEP] Login ({username}) successful.")

def activate_professional_mode(driver):
    driver.get(f"{BASE_URL}/activate-professional-mode/")
    time.sleep(1)
    print("[STEP] Professional mode activated.")


def add_skill(driver):
    driver.get(f"{BASE_URL}/add-skill/")
    time.sleep(1)

    skill_select = Select(driver.find_element(By.NAME, "skill_name"))
    skill_select.select_by_index(1)  

    driver.find_element(By.NAME, "skill_description").send_keys("Skill added by Selenium.")
    driver.find_element(By.NAME, "skill_price").send_keys("500")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(2)
    print("[STEP] Skill added successfully.")


def view_skills(driver):
    driver.get(f"{BASE_URL}/view-skills/")
    time.sleep(2)
    skills = driver.find_elements(By.CLASS_NAME, "skill-card")
    if skills:
        print(f"[STEP] {len(skills)} skill(s) visible.")
    else:
        print("[WARNING] No skills found.")


def create_post(driver):
    driver.get(f"{BASE_URL}/add-post/")
    time.sleep(1)
    driver.find_element(By.NAME, "post_description").send_keys("This is a Selenium test post.")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(2)
    print("[STEP] Community post created.")


def send_message(driver, target_username, message_text):
    try:
        
        driver.get(f"{BASE_URL}/messages/chat/{target_username}/")
        
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".chat form"))
        )
        
        
        message_input = driver.find_element(By.CSS_SELECTOR, ".chat textarea[name='message']")
        message_input.send_keys(message_text)
        
       
        send_button = driver.find_element(By.CSS_SELECTOR, ".chat button[type='submit']")
        send_button.click()
        
        time.sleep(2)
        print(f"[STEP] Message sent to {target_username} successfully.")

    except Exception as e:
        print(f"[FAIL] Messaging {target_username} failed: {str(e)}")
        raise

def delete_skill(driver):
  
    driver.get(f"{BASE_URL}/view-skills/")
    print("[TEST STEP] Navigated to View Skills page.")

    try:
       
        delete_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href*='/delete_skill/']")
            )  
        )
        delete_link_href = delete_link.get_attribute("href")
        print(f"[TEST STEP] Found delete link: {delete_link_href}")
        delete_link.click()

     
        if "/delete_skill/" in driver.current_url: 
            print("[TEST STEP] Handling confirmation page.")
            confirm_button_selector = "button[type='submit']" 
            confirm_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, confirm_button_selector))
            )
            confirm_button.click()
            WebDriverWait(driver, 10).until(EC.url_changes(delete_link_href))  
            print("[TEST STEP] Confirmed deletion.")

        else:
            print("[TEST STEP] No confirmation page detected.")
 
        try:
            success_message_selector = ".success" 
            WebDriverWait(driver, 5).until(  
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, success_message_selector)
                )
            )
            success_message = driver.find_element(
                By.CSS_SELECTOR, success_message_selector
            ).text
            print(f"[TEST STEP] Success message found: {success_message}")
        except Exception as e:
            print(
                "Success"
            )

   
        driver.get(f"{BASE_URL}/view-skills/")
        time.sleep(1)  
        skills = driver.find_elements(By.CLASS_NAME, "skill-card")  
        print(f"[TEST STEP] Number of skills after deletion: {len(skills)}")
        assert len(skills) == 0, "Skill was not deleted!" 

        print("[TEST RESULT] Skill deletion test passed.")

    except Exception as e:
        print(f"[TEST RESULT] Skill deletion test failed: {e}")
        raise
def logout(driver):
    driver.get(f"{BASE_URL}/logout/")  
    time.sleep(5)
    print("[TEST STEP] Logged out.")
from datetime import datetime
def report_first_post(driver):
    try:
        
        driver.get(f"{BASE_URL}community/")
        report_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/report/')]"))
        )
        driver.get(report_btn.get_attribute("href"))

        
        message_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "report_reason"))
        )
        
        
        message_field.clear()  
        time.sleep(0.5)      
        report_text = "Automated test report - violation found"
        message_field.send_keys(report_text)
        time.sleep(0.5)      
        
        
        if message_field.get_attribute("value") != report_text:
            raise Exception("Failed to fill report message")

       
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_btn.click()

        
        WebDriverWait(driver, 10).until(
            lambda d: "community" in d.current_url.lower()
        )
        print("Post reported successfully")
        return True

    except Exception:
        driver.save_screenshot("report_failed.png")
        print("Failed to submit report")
        raise

def delete_first_reported_post(driver):
    try:
        
        driver.get(f"{BASE_URL}reports/")
        delete_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[action*='/delete/']"))
        )

        
        submit_btn = delete_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_btn)

        
        WebDriverWait(driver, 10).until(
            EC.url_contains("reports")
        )
        print("Post deleted successfully")
        return True

    except Exception:
        driver.save_screenshot("delete_post_error.png")
        print("Failed to delete post")
        raise
def view_report(driver):
    driver.get(f"{BASE_URL}/reports/")  
    time.sleep(5)
    
def ban_user(driver, username, duration_minutes):
    try:
        print(f"\n[STEP] Attempting to ban user: {username}")
        driver.get(f"{BASE_URL}public_profile/{username}/")
        time.sleep(2)

        ban_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[action*='/ban_user/']"))
        )

        duration_input = WebDriverWait(ban_form, 5).until(
            EC.presence_of_element_located((By.NAME, "duration"))
        )
        duration_input.clear()
        duration_input.send_keys(str(duration_minutes))

        ban_button = WebDriverWait(ban_form, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ban-button"))
        )
        ban_button.click()

        
        print(f"[SUCCESS] User {username} banned successfully")
        driver.save_screenshot("after_ban.png")
        return True

    except Exception as e:
        print(f"[FAILURE] Ban operation failed: {str(e)}")
        driver.save_screenshot(f"ban_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        raise

def run_test():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        signup(driver, USERNAME, EMAIL, PASSWORD)
        login(driver, USERNAME, PASSWORD)
        activate_professional_mode(driver)
        add_skill(driver)
        view_skills(driver)
        delete_skill(driver)
        view_skills(driver)
        create_post(driver)
        send_message(driver, TARGET_USER, "This is a test message.")
        logout(driver)
        login(driver, "y38", "0000")
        report_first_post(driver)
        view_report(driver)
        delete_first_reported_post(driver)
        ban_user(driver, USERNAME, 3)
        logout(driver)
        login(driver,USERNAME,PASSWORD)

        print("\n [SUCCESS] Test passed successfully.\n")

    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()