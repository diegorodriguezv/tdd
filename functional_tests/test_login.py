from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os, poplib, time

from .base import FunctionalTest

TEST_EMAIL = "edith@example.com"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the superlist site and notices a log in section in the navbar
        # for the first time. It is telling her to enter her email address, so she does
        if self.staging_server:
            test_email = "diegortest1@gmail.com"
        else:
            test_email = TEST_EMAIL
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "Check your email", self.browser.find_element_by_tag_name("body").text
            )
        )

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has url link in it
        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"http://.*/.+$", body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text("Log out").click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL("pop.gmail.com")
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ["GMAIL_PASSWORD"])
            while time.time() - start < 60:
                # get 10 newest messages
                count, size = inbox.stat()
                print(test_email, count)
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print("getting msg", i, "of", size)
                    _, lines, _ = inbox.retr(i)
                    lines = [l.decode("utf8") for l in lines]
                    #                    for line in lines:
                    #                        if line.startswith("Subject"):
                    #                            print(line)
                    if f"Subject: {subject}" in lines:
                        email_id = i
                        body = "\n".join(lines)
                        return body
                time.sleep(5)
        except Exception as e:
            print(e)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
