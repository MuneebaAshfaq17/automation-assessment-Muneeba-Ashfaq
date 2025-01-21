import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Constants
BASE_URL = "https://reqres.in/api"
SAUCE_DEMO_URL = "https://www.saucedemo.com/"

# Configurable values
SAUCE_DEMO_CREDENTIALS = {
    "username": "visual_user",
    "password": "secret_sauce"
}

# Function to initialize the WebDriver
def initialize_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Test: Login to Sauce Demo
def test_login(credentials):
    driver = initialize_driver()
    try:
        driver.get(SAUCE_DEMO_URL)

        # Adding wait for only Demo Purpose
        # Adding wait for only Demo Purpose
        time.sleep(10)  # Keep the browser open for 10 seconds

        driver.find_element(By.ID, "user-name").send_keys(credentials["username"])
        driver.find_element(By.ID, "password").send_keys(credentials["password"])
        driver.find_element(By.ID, "login-button").click()

        assert "inventory.html" in driver.current_url, "Login failed"
        print("Login test passed!")
    finally:
        driver.quit()

# Test: Add and Remove Item from Cart
def test_add_and_remove_item(credentials):
    driver = initialize_driver()
    try:
        # Navigate to Sauce Demo login page and log in
        driver.get(SAUCE_DEMO_URL)
        driver.find_element(By.ID, "user-name").send_keys(credentials["username"])
        driver.find_element(By.ID, "password").send_keys(credentials["password"])
        driver.find_element(By.ID, "login-button").click()

        #Adding wait for only Demo Purpose
        time.sleep(10)  # Keep the browser open for 10 seconds

        # Add the first item to the cart
        driver.find_element(By.CSS_SELECTOR, ".inventory_item button").click()
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_badge.text == '1', "Item not added to cart"
        print("Item successfully added to cart.")

        # Navigate to the cart to remove the item
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Remove the item from the cart
        driver.find_element(By.CSS_SELECTOR, ".cart_button").click()

        # Adding wait for only Demo Purpose
        time.sleep(10)  # Keep the browser open for 10 seconds

        # Verify the cart is now empty
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")

        # Adding wait for only Demo Purpose
        time.sleep(10)  # Keep the browser open for 10 seconds

        assert len(cart_items) == 0, "Cart is not empty after removing the item"
        print("Item successfully removed from cart.")

    finally:
        driver.quit()

# Function to retrieve access token from the Login API
def get_access_token(email, password):
    start = time.time()
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    end = time.time()
    response_data = response.json()
    return response_data.get("token"), end - start

# Function to create a user
def create_user(name, job):
    start = time.time()
    response = requests.post(f"{BASE_URL}/users", json={"name": name, "job": job})
    end = time.time()
    response_data = response.json()
    return {**response_data, "time_taken": end - start}

# Function to update a user
def update_user(user_id, name, job):
    start = time.time()
    response = requests.put(f"{BASE_URL}/users/{user_id}", json={"name": name, "job": job})
    end = time.time()
    response_data = response.json()
    return {**response_data, "time_taken": end - start}

# Function to delete a user
def delete_user(user_id):
    start = time.time()
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    end = time.time()
    return {"status_code": response.status_code, "time_taken": end - start}

# Main Execution Block
if __name__ == "__main__":
    # Run Selenium Tests
    print("Running Selenium Tests...")
    test_login(SAUCE_DEMO_CREDENTIALS)
    test_add_and_remove_item(SAUCE_DEMO_CREDENTIALS)

    # Run API Tests
    print("\nRunning API Tests...")
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    token, time_taken = get_access_token(email, password)
    print(f"Token: {token}, Time taken: {time_taken}s")

    user_name = "Emre John"
    user_job = "Engineer"
    user = create_user(user_name, user_job)
    print(f"Created User: {user}")

    updated_user_name = "John Smith"
    updated_user_job = "Senior QA Engineer"
    updated_user = update_user(user["id"], updated_user_name, updated_user_job)
    print(f"Updated User: {updated_user}")

    delete_response = delete_user(user["id"])
    print(f"Deleted User Status Code: {delete_response['status_code']}, Time taken: {delete_response['time_taken']}s")
