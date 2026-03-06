from typing import Self

from playwright.sync_api import Page, expect


class ProjectSettingsPage:
    def __init__(self, page: Page):
        self.page = page
        self.administration_button = page.get_by_role("button", name="Administration")
        self.delete_project_button = page.get_by_role("button", name="Delete Project")
        self.toast_notification = page.get_by_text("Project will be deleted in few minutes")

    def wait_for_loaded(self) -> Self:
        expect(self.administration_button).to_be_visible()
        return self

    def click_administration(self) -> Self:
        def handle_dialog(dialog):
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.administration_button.click()
        expect(self.delete_project_button).to_be_visible()
        return self

    def delete_project(self) -> Self:
        def handle_dialog(dialog):
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.delete_project_button.click()
        return self

    def verify_deletion_toast(self) -> Self:
        expect(self.toast_notification).to_be_visible()
        return self
