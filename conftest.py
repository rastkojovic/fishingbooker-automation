import os
import pytest
from playwright.sync_api import sync_playwright, Page
from pages.sitemap_page import SitemapPage
from pages.destination_page import DestinationPage

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context(
        http_credentials = {
            "username": os.environ["FB_USERNAME"],
            "password": os.environ["FB_PASSWORD"]
        }
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def sitemap_page(page: Page) -> SitemapPage:
    return SitemapPage(page)

@pytest.fixture
def destination_page(page: Page) -> DestinationPage:
    return DestinationPage(page)