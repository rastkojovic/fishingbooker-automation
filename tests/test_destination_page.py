def test_destination_page(sitemap_page, destination_page):
    
    # Iz sekcije Top Fishing Destinations, mozeš izabrati bilo koju destinaciju.
    # Klikni na link
    sitemap_page.open()
    sitemap_page.open_top_destination("Fishing Charters in Massachusetts")

    # Sačekaj da se prikaže lista čartera (najmanje 10 kartica)
    destination_page.wait_for_charters_to_load()

    # Elementi koje je potrebno proveriti za prvu charter karticu:
    charter_index = 0

    # Naziv čartera (link/text)
    charter_name = destination_page.get_charter_name(charter_index)
    assert charter_name == "Toby Ann Charters", f"Charter name: '{charter_name}' does not match expected name: 'Toby Ann Charters'"

    # Informacija o dužini broda
    ship_length = destination_page.get_ship_length(charter_index)
    assert ship_length == "36 ft", f"Ship length: '{ship_length}' does not match expected length: '36 ft'"

    # Max broj ljudi (up to X people)
    max_crew = destination_page.get_max_crew(charter_index)
    assert max_crew == "Up to 6 people", f"Max crew: '{max_crew}' does not match expected max: 'Up to 6 people'"

    # Cena (“Trips from …”)
    price = destination_page.get_charter_price(charter_index)
    assert price == "€574", f"Price: '{price}', does not match expected price: '€574'"
    
    # Tooltip info - Hover na tooltip wishlist prikazuje očekivan info (Add listing to wishlist)
    tooltip_text = destination_page.get_wishlist_tooltip(charter_index)
    assert tooltip_text == "Add listing to wishlist"

    # TODO: “See availability” button - Ne razumem šta znači da proverim button?
    availability_button_text = destination_page.get_availability_button_text(charter_index)
    assert availability_button_text == "See availability", f"Button text: '{availability_button_text}' does not match expected text: 'See availability'!"

    # Klikni na “Sort by Price (Lowest)” filter
    destination_page.sort_by_price_lowest()

    # Pokupi cene za sve kartice i proveri da su cene sortirane rastuće
    all_prices = destination_page.get_all_prices()
    assert all_prices == sorted(all_prices), f"Prices are not in ascending order!"

    # Klikni na Sort by Price filter
    destination_page.click_sort_by_price_filter()

    # Izaberi Price (Highest) iz padajućeg menija.
    destination_page.filter_price_highest()
    # Klikni na Apply button.
    destination_page.click_filter_apply()
    # Ponovi proveru da su cene sada sortirane opadajuće
    all_prices = destination_page.get_all_prices()
    assert all_prices == sorted(all_prices, reverse=True), f"Prices are not in descending order!"
