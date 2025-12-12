def test_destination_page(sitemap_page, destination_page):
    
    # Open a top fishing destination
    sitemap_page.open()
    sitemap_page.open_top_destination("Fishing Charters in Massachusetts")
    
    destination_page.wait_for_charters_to_load()
    charter_index = 0

    # Charter name validation
    charter_name = destination_page.get_charter_name(charter_index)
    assert charter_name == "Toby Ann Charters", f"Charter name: '{charter_name}' does not match expected name: 'Toby Ann Charters'"

    # Ship length validation
    ship_length = destination_page.get_ship_length(charter_index)
    assert ship_length == "36 ft", f"Ship length: '{ship_length}' does not match expected length: '36 ft'"

    # Max crew validation
    max_crew = destination_page.get_max_crew(charter_index)
    assert max_crew == "Up to 6 people", f"Max crew: '{max_crew}' does not match expected max: 'Up to 6 people'"

    # Price validation
    price = destination_page.get_charter_price(charter_index)
    assert price == "€574", f"Price: '{price}', does not match expected price: '€574'"
    
    # Tooltip validation
    tooltip_text = destination_page.get_wishlist_tooltip(charter_index)
    assert tooltip_text == "Add listing to wishlist"

    # See availability button validation
    availability_button_text = destination_page.get_availability_button_text(charter_index)
    assert availability_button_text == "See availability", f"Button text: '{availability_button_text}' does not match expected text: 'See availability'!"

    # Sorting test
    destination_page.sort_by_price_lowest()
    all_prices = destination_page.get_all_prices()
    assert all_prices == sorted(all_prices), f"Prices are not in ascending order!"
    destination_page.click_sort_by_price_filter()
    destination_page.filter_price_highest()
    destination_page.click_filter_apply()
    all_prices = destination_page.get_all_prices()
    assert all_prices == sorted(all_prices, reverse=True), f"Prices are not in descending order!"
