from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10
POLL_INTERVAL = 0.5


class NewVisitorTest(LiveServerTestCase):
    # TODO: Adjust model so that items are associated with different lists
    # TODO: Add unique urls for each list
    # TODO: Add a url for creating a new list via post
    # TODO: Add urls for adding a new item to an existing list via post
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_can_start_a_list_for_one_user(self):
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
        self.wait_for_row_in_table("1: play piano")

        # He enters "practice yoga"
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("practice yoga")

        # He hits enter and the task is added
        inputbox.send_keys(Keys.ENTER)

        # The page shows both tasks
        self.wait_for_row_in_table("1: play piano")
        self.wait_for_row_in_table("2: practice yoga")

        # profit!

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Diego starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("play piano")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: play piano")

        # He notices that his list has a unique url
        list_url = self.browser.current_url
        self.assertRegex(list_url, "/lists/.+")

        # Fernando comes to the site
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # There is no sign of Diego's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("play piano", page_text)
        self.assertNotIn("practice yoga", page_text)

        # Fernando starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("tdd")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: tdd")

        # Fernando gets his own unique url
        list_url_2 = self.browser.current_url
        self.assertRegex(list_url_2, "/lists/.+")
        self.assertNotEqual(list_url, list_url_2)

        # There is no sign of Diego's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("play piano", page_text)
        self.assertIn("tdd", page_text)

        # double profit

    def wait_for_row_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(POLL_INTERVAL)

    def tearDown(self):
        self.browser.quit()
