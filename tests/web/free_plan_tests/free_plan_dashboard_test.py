import pytest
from playwright.sync_api import expect

from web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_overview_projects_page_header(free_project_app: Application):
    dashboard = free_project_app.dashboard_page
    dashboard.wait_for_loaded()
    expect(dashboard.company_dropdown).to_contain_text("Free Projects")
    expect(dashboard.create_company_link).to_be_visible()

    expect(dashboard.plan_tooltip).to_have_text("free plan")
    dashboard.plan_tooltip.hover(timeout=500)
    expect(free_project_app.page.get_by_text("You have a free subscription")).to_be_visible()

    dashboard.search_project("My Awesome Project")
    expect(dashboard.search_input).to_have_value("My Awesome Project")


@pytest.mark.regression
@pytest.mark.web
def test_overview_free_plan_dashboard_elements(free_project_app: Application):
    dashboard = free_project_app.dashboard_page
    dashboard.wait_for_loaded()
    expect(dashboard.no_project_image).to_be_visible()
    expect(dashboard.empty_state_message).to_be_visible()
    expect(dashboard.empty_state_create_project_button).to_be_visible()
    dashboard.verify_educational_videos()
    expect(dashboard.docs_link).to_have_attribute("href", "https://docs.testomat.io")
