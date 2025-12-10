from playwright.sync_api import Page

class BasePage:
    
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
        self.page.goto(url)

    def wait_for_network_idle(self) -> None:
        """
        Wait until the page finishes all active network requests.
        Ensure the page has finished loading all dynamic content.
        """
        self.page.wait_for_load_state("networkidle")