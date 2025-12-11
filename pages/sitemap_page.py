from pages.base_page import BasePage
from playwright.sync_api import Locator

class SitemapPage(BasePage):
    URL = "https://nextjs15.dev.fishingbooker.com/sitemap"

    @property
    def top_destinations_root(self) -> Locator:
        return self.page.locator("(//div[contains(@class,'list-items-spacing')])[1]")
    
    def open(self) -> None:
        super().open(self.URL)

    def open_top_destination(self, destination_name: str) -> None:
        """
        Opens a link in the 'Top Fishing Destinations' section based on full destination name (e.g. 'Fishing Charters in Key West').
        """
        self.top_destinations_root.get_by_role("link", name=destination_name).click()
        self.wait_for_network_idle()