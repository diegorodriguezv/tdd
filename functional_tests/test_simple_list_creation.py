from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # Diego likes to do lists
        self.browser.get(self.live_server_url)

        # He finds to-do in the title
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # He wants to add a task
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # He adds "play piano"
        inputbox.send_keys("play piano")

        # He hits enter and the task is added
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: play piano")

        # He enters "practice yoga"
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
