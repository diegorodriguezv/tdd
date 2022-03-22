from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Diego likes to do lists
        self.browser.get("http://localhost:8000")

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

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(
            any(row.text == "1: play piano" for row in rows),
            "New to do item did not appear in table",
        )

        # He enters "practice yoga"
        self.fail("Finish the test!")

        # He hits enter and the task is added

        # The page shows both tasks

        # Ths site has generated a unique url and shows text explaining that

        # He visits the url, both tasks are there

        # profit!

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
