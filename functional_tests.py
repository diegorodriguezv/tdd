from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Diego likes to do lists
        self.browser.get("http://localhost:8000")

        # He finds to-do in the title
        self.assertIn("To-Do", self.browser.title)
        self.fail('Finish the test!')

        # He wants to add a task

        # He adds "play piano"

        # He hits enter and the task is added

        # He enters "practice yoga"

        # He hits enter and the task is added

        # The page shows both tasks

        # Ths site has generated a unique url and shows text explaining that

        # He visits the url, both tasks are there

        # profit!

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
