from typing import Self

from playwright.sync_api import Page, expect


class CrispChat:
    def __init__(self, page: Page):
        self.page = page
        self.chat_button = page.locator("#crisp-chatbox").get_by_role("button")
        self.close_chat_button = page.locator("#crisp-chatbox-button")

        self.chat_window = page.locator("#crisp-chatbox-chat")
        self.chat_tab = self.chat_window.get_by_role("button", name="Chat")
        self.search_tab = self.chat_window.get_by_role("button", name="Search")

        self.message_input = self.chat_window.get_by_placeholder("Compose your message...")
        self.send_button = self.chat_window.get_by_role("button", name="Send")
        self.emoji_button = self.chat_window.get_by_label("Insert an emoji")
        self.attach_file_button = self.chat_window.get_by_label("Send a file")

        self.last_operator_message = self.chat_window.locator(".cc-nb9p2--operator .cc-1yk1e").last

    def wait_for_loaded(self) -> Self:
        expect(self.chat_button).to_be_visible()
        return self

    def open(self) -> Self:
        if not self.is_visible:
            self.chat_button.click()
            expect(self.chat_window).to_be_visible()
        return self

    def close(self) -> Self:
        if self.is_visible:
            self.close_chat_button.click()
            expect(self.chat_window).not_to_be_visible()
        return self

    def close_search_form(self) -> Self:
        self.close_search_form_button.click()
        return self

    def send_message(self, message: str) -> Self:
        self.message_input.fill(message)
        self.send_button.click()
        return self

    def get_last_message_text(self) -> str:
        return self.last_operator_message.inner_text()

    def switch_to_search(self) -> Self:
        self.search_tab.click()
        return self

    def switch_to_chat(self) -> Self:
        self.chat_tab.click()
        return self

    @property
    def is_maximized(self) -> bool:
        return self.chat_button.get_attribute("data-maximized") == "true"

    @property
    def is_visible(self) -> bool:
        return self.chat_window.is_visible()
