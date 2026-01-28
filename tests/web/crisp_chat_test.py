import pytest
from playwright.sync_api import expect

from src.web import Application
from tests.fixtures.config import Config


@pytest.mark.web
def test_crisp_chat_overview(logged_app: Application, configs: Config):
    logged_app.dashboard_page.wait_for_loaded()
    chat = logged_app.crisp_chat.wait_for_loaded()
    chat.open()

    expect(chat.chat_window).to_be_visible()
    expect(chat.message_input).to_be_visible()
    expect(chat.messages_tab).to_be_visible()
    expect(chat.search_tab).to_be_visible()
    expect(chat.attach_file_button).to_be_visible()
    expect(chat.emoji_button).to_be_visible()
    expect(chat.greeting_message).to_be_visible()

    test_message = "Hello, this is a test message."
    chat.message_input.fill(test_message)
    expect(chat.message_input).to_have_value(test_message)

    chat.switch_to_search()
    chat.switch_to_messages()
    expect(chat.message_input).to_be_visible()
    chat.close()
    expect(chat.chat_toggle).to_have_attribute("data-maximized", "false")
