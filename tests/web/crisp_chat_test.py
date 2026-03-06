import os

import pytest
from playwright.sync_api import expect

from src.web import Application
from tests.fixtures.config import Config


@pytest.mark.regression
@pytest.mark.skipif(os.getenv("CI") == "true", reason="Crisp chat widget does not load in headless/CI environments")
def test_crisp_chat_overview(isolated_logged_app: Application, configs: Config):
    isolated_logged_app.dashboard_page.wait_for_loaded()
    chat = isolated_logged_app.crisp_chat.wait_for_loaded()

    chat.open().start_chat(configs.email)

    expect(chat.message_input).to_be_visible()
    expect(chat.messages_tab).to_be_visible()
    expect(chat.search_tab).to_be_visible()
    expect(chat.attach_file_button).to_be_visible()
    expect(chat.emoji_button).to_be_visible()
    expect(chat.container.get_by_text("How can we help you")).to_be_visible()

    test_message = "Hello, this is a test message."
    chat.message_input.fill(test_message)
    expect(chat.message_input).to_have_value(test_message)

    chat.switch_to_search()
    expect(chat.message_input).to_be_hidden()

    chat.switch_to_messages()
    expect(chat.message_input).to_be_visible()

    chat.close()
    expect(chat.container.locator(".cc-18ov6")).to_have_attribute("data-maximized", "false")
