import pytest
from playwright.sync_api import expect

from web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(free_project_app: Application):
    expect(free_project_app.page.get_by_text("You have not created any projects yet")).to_be_visible()
    expect(free_project_app.page.get_by_text("Free plan")).to_be_visible()
    expect(free_project_app.dashboard_page.plan_tooltip).to_have_text("free plan")
    free_project_app.dashboard_page.plan_tooltip.hover(timeout=500)
    expect(free_project_app.page.get_by_text("You have a free subscription")).to_be_visible()
