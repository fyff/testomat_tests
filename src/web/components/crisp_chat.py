from typing import Self

from playwright.sync_api import Page, expect


class CrispChat:
    def __init__(self, page: Page):
        self.page = page
        self.chat_toggle = page.locator("#crisp-chatbox").locator(".cc-18ov6")
        self.chat_window = page.locator("#crisp-chatbox")
        self.messages_tab = page.get_by_role("button", name="Messages")
        self.search_tab = page.get_by_role("button", name="Search")
        self.message_input = page.get_by_placeholder("Compose your message...")
        self.send_button = page.get_by_role("button", name="Send")
        self.emoji_button = page.get_by_label("Insert an emoji")
        self.attach_file_button = page.get_by_label("Send a file")
        self.greeting_message = page.get_by_text("How can we help you with testomat.io?")
        self.email_alert = page.get_by_text("Please set your email to continue.")  # Changed to get_by_text
        self.crisp_email_input = page.get_by_role("textbox", name="Enter your email address...")
        self.set_my_email_button = page.get_by_role("button", name="Set my email")

    def wait_for_loaded(self) -> Self:
        expect(self.chat_toggle).to_be_visible(timeout=10000)
        return self

    def open(self) -> Self:
        if self.chat_toggle.get_attribute("data-maximized") == "false":
            self.chat_toggle.click(force=True)

        expect(self.chat_toggle).to_have_attribute("data-maximized", "true")
        return self

    def close(self) -> Self:
        if self.chat_toggle.get_attribute("data-maximized") == "true":
            self.chat_toggle.click(force=True)

        expect(self.chat_toggle).to_have_attribute("data-maximized", "false")
        return self

    def start_chat(self, email: str) -> Self:
        self.email_alert.click()
        self.crisp_email_input.fill(email)
        self.set_my_email_button.click()
        expect(self.message_input).to_be_enabled()
        return self

    def send_message(self, message: str) -> Self:
        expect(self.message_input).to_be_enabled()
        self.message_input.fill(message)
        self.send_button.click()
        return self

    def switch_to_search(self) -> Self:
        self.search_tab.click(force=True)
        return self

    def switch_to_messages(self) -> Self:
        self.messages_tab.click(force=True)
        return self

    @property
    def is_visible(self) -> bool:
        return self.chat_toggle.get_attribute("data-maximized") == "true"
