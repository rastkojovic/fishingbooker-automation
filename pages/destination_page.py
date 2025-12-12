from pages.base_page import BasePage
from playwright.sync_api import Locator, expect


class DestinationPage(BasePage):

    @property
    def charter_cards(self) -> Locator:
        return self.page.get_by_test_id("single-charter-card-container")
    
    @property
    def filter_dialog(self) -> Locator:
        return self.page.get_by_role("dialog")

    def wait_for_charters_to_load(self, timeout_ms:int = 10000) -> None:
        '''
        Waits until the number of charter cards is >= 10
        '''
        cards = self.charter_cards
        expect(cards.nth(9)).to_be_visible(timeout=timeout_ms)

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

    def _extract_price_from_str(self, char_string: str) -> int:
        """
        Removes all non-digit characters from string and returns an int
        ex. € 1,234 -> 1234
        """
        digits = "".join(char for char in char_string if char.isdigit())
        if not digits:
            raise ValueError(f"No digits found in price text: '{char_string}'")
        return int(digits)


    def get_all_prices(self) -> list[int]:
        price_elements = self.page.get_by_test_id("charter-card-trip-from-container").get_by_text("€")
        text_prices = price_elements.all_inner_texts()

        prices: list[int] = []
        for char in text_prices:
            current_price = self._extract_price_from_str(char)
            prices.append(current_price)

        return prices
    
    def get_wishlist_button(self, index: int = 0) -> Locator:
        return self._card(index).get_by_test_id("add-to-wishlist")
    
    def get_wishlist_tooltip(self, index: int = 0) -> str:
        button = self.get_wishlist_button(index)
        button.hover()

        tooltip_root = self.page.locator("xpath=//div[contains(@style, 'position: absolute')]/div[@elevation='2']")
        tooltip_root.wait_for(state="visible", timeout=3000)
        tooltip_text = tooltip_root.locator("xpath=.//div[normalize-space(text())!='']")
        tooltip_text.wait_for(state="visible", timeout=3000)
        return tooltip_text.inner_text().strip()

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