import pytest
from playwright.sync_api import expect

from src.web.application import Application
from tests.fixtures.config import Config


@pytest.mark.web
def test_crisp_chat_overview(logged_app: Application, configs: Config):
    logged_app.dashboard_page.wait_for_loaded()
    chat = logged_app.crisp_chat
    chat.wait_for_loaded().open()

    expect(chat.chat_window).to_be_visible()
    expect(chat.message_input).to_be_visible()
    expect(chat.chat_tab).to_be_visible()
    expect(chat.search_tab).to_be_visible()
    expect(chat.attach_file_button).to_be_visible()
    expect(chat.emoji_button).to_be_visible()
    expect(chat.last_operator_message).to_contain_text("How can we help you with testomat.io?")

    test_message = "Hello, this is a test message."
    chat.message_input.fill(test_message)
    expect(chat.message_input).to_have_value(test_message)
    # chat.send_button.click()
    # TODO serch pop-up
    # chat.switch_to_search()
    # chat.close_search_form()
    expect(chat.message_input).to_be_visible()
    logged_app.page.pause()
    chat.close()
    expect(chat.chat_window).not_to_be_visible()
