from pages.base_page import BasePage
from playwright.sync_api import Locator
import time


class DestinationPage(BasePage):

    @property
    def charter_cards(self) -> Locator:
        return self.page.get_by_test_id("single-charter-card-container")
    
    @property
    def filter_dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    def wait_for_charters_to_load(self, min_cards: int = 10, timeout: int = 10) -> None:
        '''
        Waits until the number of charter cards is >= 10
        '''
        start = time.time()

        while True:
            count = self.charter_cards.count()

            if count >= min_cards:
                return
            
            if time.time() - start > timeout:
                raise TimeoutError(
                    f"Timeout! Expected at least {min_cards} but got {count}!"
                )
            
            time.sleep(0.1)

    def _card(self, index: int = 0) -> Locator:
        return self.charter_cards.nth(index)
    
    def get_charter_name(self, index: int = 0) -> str:
        return self._card(index).get_by_test_id("charter-card-title").inner_text()

    def get_ship_length(self, index: int = 0) -> str:
        return self._card(index).locator("xpath=.//div[@data-testid='charter-card-boat-silhouette']/div/p/span").inner_text()

    def get_max_crew(self, index: int = 0) -> str:
        return self._card(index).locator("xpath=.//div[@data-testid='charter-card-boat-silhouette']/p/span").inner_text()

    def get_charter_price(self, index: int = 0) -> str:
        return self._card(index).get_by_test_id("charter-card-trip-from-container").get_by_text("€").inner_text()

    def click_see_availability(self, index: int = 0) -> None:
        self._card(index).get_by_test_id("charter-card-see-availability-button").click()

    def get_availability_button_text(self, index: int = 0) -> str:
        return self._card(index).get_by_test_id("charter-card-see-availability-button").inner_text()

    def click_sort_by_price_filter(self):
        self.page.get_by_role("button", name="Sort by Price (Lowest)").click()

    def sort_by_price_lowest(self) -> None:
        self.page.get_by_test_id("sort-price-lowest-button").click()

    def sort_by_price_highest(self) -> None:
        self.page.get_by_test_id("sort-price-highest-button").click()

    def sort_by_reviews_highest(self) -> None:
        self.page.get_by_test_id("sort-reviews-highest-button").click()

    def sort_by_recommended(self) -> None:
        self.page.get_by_test_id("sort-recommended-button").click()

    def get_all_prices(self) -> list[float]:
        price_elements = self.page.get_by_test_id("charter-card-trip-from-container").get_by_text("€")
        text_prices = price_elements.all_inner_texts()

        prices: list[float] = []
        for t in text_prices:
            current_price = float(t.split("€")[1])
            prices.append(current_price)

        return prices
    
    def get_wishlist_button(self, index: int = 0) -> Locator:
        return self._card(index).get_by_test_id("add-to-wishlist")
    
    def get_wishlist_tooltip(self, index: int = 0) -> str:
        button = self.get_wishlist_button(index)
        button.hover()

        tooltip_root = self.page.locator("div[elevation='2']")
        tooltip_root.wait_for(state="visible", timeout=3000)
        tooltip_text = tooltip_root.locator("div").last
        return tooltip_text.inner_text()

    # Filter Dialog
    def filter_price_highest(self):
        self.filter_dialog.locator("#-price").check()

    def filter_price_lowest(self):
        self.filter_dialog.locator("#price").check()

    def filter_recommended(self):
        self.filter_dialog.locator("#-recommended").check()

    def filter_reviews(self):
        self.filter_dialog.locator("#-review").check()

    def click_filter_apply(self):
        self.filter_dialog.get_by_role("button", name="Apply").click()