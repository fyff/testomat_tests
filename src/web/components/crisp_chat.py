from typing import Self

from playwright.sync_api import Page, expect


class CrispChat:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.locator("#crisp-chatbox")
        self.chat_toggle = self.container.locator(".cc-18ov6")
        self.chat_window = self.container.locator("[data-maximized='true']")

        self.messages_tab = self.container.get_by_role("button", name="Messages")
        self.search_tab = self.container.get_by_role("button", name="Search")
        self.message_input = self.container.get_by_placeholder("Compose your message...")
        self.send_button = self.container.get_by_role("button", name="Send")
        self.emoji_button = self.container.get_by_label("Insert an emoji")
        self.attach_file_button = self.container.get_by_label("Send a file")
        self.greeting_message = self.container.get_by_text("How can we help you with testomat.io?")
        self.email_alert = self.container.get_by_text("Please set your email to continue.")
        self.crisp_email_input = self.container.get_by_role("textbox", name="Enter your email address...")
        self.set_my_email_button = self.container.get_by_role("button", name="Set my email")

    def wait_for_loaded(self) -> Self:
        expect(self.container).to_be_attached(timeout=15000)
        expect(self.chat_toggle).to_be_attached(timeout=5000)
        return self

    def open(self) -> Self:
        if not self.is_visible:
            self.chat_toggle.click(force=True)

        expect(self.chat_toggle).to_have_attribute("data-maximized", "true", timeout=10000)
        return self

    def close(self) -> Self:
        if self.is_visible:
            self.chat_toggle.click(force=True)

        expect(self.chat_toggle).to_have_attribute("data-maximized", "false", timeout=10000)
        return self

    def start_chat(self, email: str) -> Self:
        if self.email_alert.is_visible():
            self.email_alert.click()
            self.crisp_email_input.fill(email)
            self.set_my_email_button.click()

        expect(self.message_input).to_be_visible()
        return self

    def send_message(self, message: str) -> Self:
        expect(self.message_input).to_be_enabled()
        self.message_input.fill(message)
        self.send_button.click()
        return self

    def switch_to_search(self) -> Self:
        self.search_tab.click()
        return self

    def switch_to_messages(self) -> Self:
        self.messages_tab.click()
        return self

    @property
    def is_visible(self) -> bool:
        return self.container.locator(".cc-18ov6").get_attribute("data-maximized") == "true"
