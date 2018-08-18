import unittest
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import argparse
import random

class RateBook(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(r"chromedriver.exe")

    def test_search_in_python_org(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        driver.implicitly_wait(10)
        driver.get("https://www.goodreads.com/")

        user_email = "sadarua+1@gmail.com"
        user_pass = "test123456"

        assert len(user_email) > 1 and len(user_pass) > 1

        home_email = driver.find_element_by_id("userSignInFormEmail")
        home_email.send_keys(user_email)

        home_pass = driver.find_element_by_id("user_password")
        home_pass.send_keys(user_pass+"d")

        sign_in = driver.find_element_by_xpath("//*[@id='sign_in']/div[3]/input[1]")
        sign_in.click()

        wait.until(EC.visibility_of(driver.find_element(By.XPATH, "//*[@id='emailForm']/p")))
        assert driver.find_element_by_xpath("//*[@id='emailForm']/p").is_displayed()

        #SIGH IN CORRECT

        password_field = driver.find_element_by_id("user_password")
        password_field.send_keys(user_pass)

        sign_in_btn = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/form/fieldset/div[5]/input")
        sign_in_btn.click()

        #SEARCH
        search_field = driver.find_element_by_css_selector(".searchBox__input.searchBox__input--navbar")
        search_field.send_keys("Best crime and mystery books")
        search_field.send_keys(Keys.ENTER)

        #RESULTS

        book_block_list = driver.find_elements_by_css_selector(".tableList > tbody > tr")
        for i in range(0, 3):
            want_to_read = book_block_list[i].find_element_by_css_selector("td > div > div:nth-of-type(1)")
            want_to_read.click()

            wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[1]/form/button/span[2]")))

            drop_down = book_block_list[i].find_element_by_css_selector("td > div > div:nth-of-type(2)")
            drop_down.click()
            wait.until(EC.visibility_of(drop_down.find_element_by_css_selector("div > div > ul> li:nth-child(1) > button")))

            mark_read = driver.find_element_by_css_selector(".wtrShelfMenu > div:nth-of-type(1) > ul:nth-of-type(1) > li:nth-of-type(1)")
            mark_read.click()

            wait.until(
                EC.visibility_of(driver.find_element_by_css_selector("#boxContents:nth-of-type(2)")))

            rating_stars = driver.find_elements_by_xpath("//*[@id='boxContents']//div[@class='stars']//a")
            stars = random.randint(1, len(rating_stars))
            rating_stars[stars-1].click()
            driver.implicitly_wait(5)

            start_year = Select(driver.find_element_by_css_selector(".rereadDatePicker.smallPicker.startYear"))
            start_year.select_by_visible_text("2018")

            start_month = Select(driver.find_element_by_css_selector(".rereadDatePicker.largePicker.startMonth"))
            month = random.randint(2, len(driver.find_elements_by_css_selector(".rereadDatePicker.largePicker.startMonth > option")) - 2)
            start_month.select_by_index(month)

            start_day = Select(driver.find_element_by_css_selector(".rereadDatePicker.smallPicker.startDay"))
            days = random.randint(2, len(driver.find_elements_by_css_selector(".rereadDatePicker.smallPicker.startDay > option")) - 2)
            start_day.select_by_index(days)

            date_finished = driver.find_element_by_css_selector(".endedAtSetTodayLink.gr-button")
            date_finished.click()

            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".formItem > .gr-button")))
            save = driver.find_element_by_css_selector(".formItem > .gr-button")
            save.click()
            time.sleep(2)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()