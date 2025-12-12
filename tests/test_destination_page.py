from playwright.sync_api import expect
import re

def test_destination_page(sitemap_page, destination_page):
    
    # Open a top fishing destination
    sitemap_page.open()
    sitemap_page.open_top_destination("Fishing Charters in Honolulu")

    destination_page.wait_for_charters_to_load()
    charter_index = 3

    # CHARTER NAME VALIDATION
    charter_name_link = destination_page.get_charter_name_link(charter_index)
    expect(charter_name_link).to_be_visible()
    charter_name_text = charter_name_link.inner_text().strip()
    assert charter_name_text, f"Charter name text is empty!"
    expect(charter_name_link).to_have_attribute("href", re.compile("/charters/view/"))

    # SHIP LENGTH VALIDATION
    ship_length = destination_page.get_ship_length(charter_index)
    expect(ship_length).to_be_visible()
    ship_length_str = ship_length.inner_text().strip()
    assert ship_length_str, f"Ship length text is empty!"
    ship_length_value = destination_page._extract_digits(ship_length_str)
    assert ship_length_value > 0, f"Ship length must be greater than 0! Value:'{ship_length_value}'"
    assert 'ft' in ship_length_str.lower(), f"Ship length does not contain expected unit 'ft'! Value:'{ship_length_str}'"

    # MAX CREW VALIDATION
    max_crew = destination_page.get_max_crew(charter_index)
    expect(max_crew).to_be_visible()
    crew_text = max_crew.inner_text().strip()
    assert crew_text, f"Max number of people info is empty!"
    assert 'people' in crew_text.lower(), f"Max number of people text is missing the word 'people' Value:'{crew_text}'"
    crew_value = destination_page._extract_digits(crew_text)
    assert crew_value > 0, f"Max crew needs to be greater than 0! Value:'{crew_value}'"

    # PRICE VALIDATION
    price = destination_page.get_charter_price(charter_index)
    expect(price).to_be_visible()
    price_text = price.inner_text().strip()
    assert price_text, f"Charter price info is missing!"
    assert '€' in price_text, f"Charter price does not contain currency symbol! Value:'{price_text}'"
    price_value = destination_page._extract_digits(price_text)
    assert price_value > 0, f"Charter price must be greater than 0! Value:'{price_value}'"
    
    # TOOLTIP VALIDATION
    tooltip_text = destination_page.get_wishlist_tooltip_str(charter_index)
    assert tooltip_text == "Add listing to wishlist", f"Unexpected tooltip text: '{tooltip_text}'"

    # 'SEE AVAILABILITY' BUTTON VAIDATION
    availability_button = destination_page.get_availability_button(charter_index)
    expect(availability_button).to_be_visible()
    expect(availability_button).to_have_attribute("href", re.compile("/charters/view/"))
    button_href = availability_button.get_attribute("href")
    button_text = availability_button.inner_text().strip()
    assert button_text == "See availability", f"Unexpected button text: '{button_text}'!"

    with destination_page.page.context.expect_page() as new_page_info:
        availability_button.click()
    new_tab = new_page_info.value
    expect(new_tab).to_have_url(re.compile(button_href))
    new_tab.close()
    destination_page.page.bring_to_front()

    # SORTING VALIDATION
    destination_page.sort_by_price_lowest()
    all_prices = destination_page.get_all_prices()
    assert all_prices == sorted(all_prices), f"Prices are not in ascending order!"
    destination_page.click_sort_by_price_filter()
    destination_page.filter_price_highest()
    destination_page.click_filter_apply()
    all_prices = destination_page.get_all_prices()
    assert all_prices == sorted(all_prices, reverse=True), f"Prices are not in descending order!"
