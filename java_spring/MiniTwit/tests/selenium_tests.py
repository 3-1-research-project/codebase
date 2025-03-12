import unittest
from random import choice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from string import ascii_letters


class MiniTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(executable_path="/root/chromedriver",options=options)
        self.rand_username = ''.join(choice(ascii_letters) for _ in range(10))
        self.rand_password = ''.join(choice(ascii_letters) for _ in range(10))

    def test_register_login(self):
        driver = self.driver
        driver.get("http://146.190.207.33:8081/public")

        elem = driver.find_element(By.LINK_TEXT, "sign up")
        elem.click()
        self.assertIn("Sign Up", driver.title)

        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_all_elements_located((By.NAME, 'username')))

        driver.find_element(By.NAME, 'username').send_keys(self.rand_username)
        driver.find_element(By.NAME, 'email').send_keys(f"{self.rand_username}@test.dk")
        driver.find_element(By.NAME, 'password').send_keys(self.rand_username)
        repass_input = driver.find_element(By.NAME, 'password2')
        repass_input.send_keys(self.rand_username)
        repass_input.send_keys(Keys.RETURN)

        self.assertIn("Sign In", driver.title)

        driver.find_element(By.NAME, 'username').send_keys(self.rand_username)
        pass_input = driver.find_element(By.NAME, 'password')
        pass_input.send_keys(self.rand_username)
        pass_input.send_keys(Keys.RETURN)

        self.assertIn("my favourites", driver.page_source)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
