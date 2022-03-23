from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    # TODO: Remove time.sleep
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Diego likes to do lists
        self.browser.get(self.live_server_url)

        # He finds to-do in the title
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # He wants to add a task
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # He adds "play piano"
        inputbox.send_keys("play piano")

        # He hits enter and the task is added
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_table("1: play piano")

        # He enters "practice yoga"
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("practice yoga")

        # He hits enter and the task is added
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page shows both tasks
        self.check_for_row_in_table("1: play piano")
        self.check_for_row_in_table("2: practice yoga")

        # Ths site has generated a unique url and shows text explaining that
        self.fail("Finish the test!")

        # He visits the url, both tasks are there

        # profit!

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def tearDown(self):
        self.browser.quit()
