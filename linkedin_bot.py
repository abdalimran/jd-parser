from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pickle
import re

DELAY = 5

def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver
    
def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def login(driver, email, password):
        driver.maximize_window()
        driver.get('https://www.linkedin.com/login')
        time.sleep(DELAY)

        driver.find_element(By.ID, 'username').send_keys(email)
        driver.find_element(By.ID, 'password').send_keys(password)

        driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
        time.sleep(DELAY)
        
        return driver

def search_linkedin(driver, keywords, location):
    driver.get("https://www.linkedin.com/jobs/")
    
    try:
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search-box__text-input')))
    except TimeoutException:
        pass
    
    time.sleep(DELAY)

    search_keywords = driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-keyword-id-')]")
    search_keywords.send_keys(keywords)
    time.sleep(DELAY)
    
    search_location = driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-location-id-')]")
    search_location.send_keys(location)
    time.sleep(DELAY)
    
    search_location.send_keys(Keys.RETURN)
    time.sleep(DELAY)

    return driver

def scroll_to(driver, job_list_item):
    driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
    job_list_item.click()
    time.sleep(DELAY)
    return driver

def get_job_data(driver, job):
    job_id = job.find_element(By.CLASS_NAME, 'job-card-container').get_attribute('data-job-id')
    metadata = job.find_element(By.XPATH, "//*[contains(@class, 'jobs-unified-top-card__content')]").get_attribute('textContent')
    metadata = re.sub(r'(\s*\n) +', '***', metadata.strip()).split('***')
    details = driver.find_element(By.ID, "job-details").text
    return {'job_id':job_id, 'metadata':metadata, 'job_description':details}