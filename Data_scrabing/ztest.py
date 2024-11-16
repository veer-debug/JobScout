from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# Set up WebDriver (Assuming you have already done this)
driver = webdriver.Chrome()

# Navigate to the page
driver.get('https://razorpay.com/jobs/jobs-all/?location=all&department=')

# Wait for the element to be clickable
try:
    ck = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "styles_right__NhIcm"))
    )
    
    # Scroll the element into view before clicking
    driver.execute_script("arguments[0].scrollIntoView(true);", ck)

    # Option 1: Click with ActionChains to handle overlapping elements
    action = ActionChains(driver)
    action.move_to_element(ck).click().perform()

    # Option 2: If ActionChains still fails, use JavaScript to click
    # driver.execute_script("arguments[0].click();", ck)

except TimeoutException:
    print("Element not found within the given time")
except ElementClickInterceptedException:
    print("Element is being blocked by another element")

# Close the driver (optional)
driver.quit()
