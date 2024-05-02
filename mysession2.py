import reservationapi
import configparser
import time
import json

def load_configuration(file_path):
    """Load the configuration file containing the URLs and keys."""
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def initialize_api(config):
    """Create an API object to communicate with the hotel API."""
    hotel = reservationapi.ReservationApi(
        config['hotel']['url'],
        config['hotel']['key'],
        int(config['global']['retries']),
        float(config['global']['delay'])
    )
    band = reservationapi.ReservationApi(
        config['band']['url'],
        config['band']['key'],
        int(config['global']['retries']),
        float(config['global']['delay'])
    )
    return hotel, band

def check_common_slots(hotel_api, band_api):
    """Check the availability of common slots and display the first 20."""
    common_slots = []
    hotel_slots = hotel_api._send_request("getAvailable", "")
    band_slots = band_api._send_request("getAvailable", "")

    # Extract the IDs of common slots
    for slot in hotel_slots:
        if slot['id'] in [b_slot['id'] for b_slot in band_slots]:
            common_slots.append({"id": slot['id']})
            if len(common_slots) == 20:
                break

    print("\nThe first 20 common slots where hotel and band slots are available.\n")
    print(json.dumps(common_slots))
    return common_slots

def display_current_slots(api):
    """Display the current slots booked by the user."""
    print("\nCurrent slots resereved by you:\n")
    print(json.dumps(api._send_request("getHold", "")))

def reserve_earliest_common_slot(hotel_api, band_api, common_slots):
    """Reserve the earliest common slot and release higher slot if necessary."""
    current_slots = hotel_api._send_request("getHold", "")
    
    
    if not current_slots:
        # If no current slots booked, reserve the earliest common slot
        earliest_slot = common_slots[0]['id']
        print(f"\nReserving earliest common slot: {earliest_slot}\n")
        hotel_api._send_request("postHold", earliest_slot)
        band_api._send_request("postHold", earliest_slot)
        print(f"\nYou have reserved slot: {earliest_slot}")
        display_current_slots(hotel_api)
    else:
        current_slot_ids = [slot['id'] for slot in current_slots]
        earliest_common_slot_id = common_slots[0]['id']

        # Reserve the earliest common slot
        print(f"\nReserving earliest common slot: {earliest_common_slot_id}\n")
        hotel_api._send_request("postHold", earliest_common_slot_id)
        print(f"Hotel was successfully reserved at slot {earliest_common_slot_id}")
        band_api._send_request("postHold", earliest_common_slot_id)
        print(f"Band was successfully reserved at slot {earliest_common_slot_id}\n")
        print(f"You have reserved slot: {earliest_common_slot_id}")
        display_current_slots(hotel_api)

        # Release higher slot if necessary
        if len(current_slot_ids) == 1:
            higher_slot = max(current_slot_ids)

            slot_reserved = int(higher_slot)
            new_slot_reserved = int(earliest_common_slot_id)
            reservation_to_delete = max(slot_reserved, new_slot_reserved)

            if higher_slot != earliest_common_slot_id:
                print(f"\nReleasing later slot: {reservation_to_delete}\n")
                hotel_api._send_request("delete", reservation_to_delete)
                band_api._send_request("delete", reservation_to_delete)
                print(f"You have released slot: {reservation_to_delete}")
                display_current_slots(hotel_api)


def recheck_for_earlier_bookings(hotel_api, band_api):
    """Recheck for earlier bookings."""
    print("\nRechecking for earlier reservation slots...\n")

    # Checking for errors when maybe 2 hotel slots are reserved and only 1 band slot reserved
    handle_slot_discrepancies(hotel_api, band_api)
    
    # Fetch the latest list of common slots
    common_slots = check_common_slots(hotel_api, band_api)
    
    # Reserve earliest common slot and release higher slot if necessary
    reserve_earliest_common_slot(hotel_api, band_api, common_slots)
    
    # print("\nRechecking for earlier resrvation slots completed.\n")

def handle_slot_discrepancies(hotel_api, band_api):
    """Handle discrepancies in booked slots between hotel and band."""
    hotel_slots = hotel_api._send_request("getHold", "")
    band_slots = band_api._send_request("getHold", "")

    discrepancies_found = False

    if len(hotel_slots) == 1:
        # If hotel has 2 slots booked, cancel the unmatched band slot
        for slot in band_slots:
            if slot['id'] not in [h_slot['id'] for h_slot in hotel_slots]:
                print(f"Cancelling band slot {slot['id']}...")
                band_api._send_request("delete", slot['id'])
                print(f"Band slot {slot['id']} cancelled.")
                discrepancies_found = True
                break

    elif len(band_slots) == 1:
        # If band has 2 slots booked, cancel the unmatched hotel slot
        for slot in hotel_slots:
            if slot['id'] not in [b_slot['id'] for b_slot in band_slots]:
                print(f"Cancelling hotel slot {slot['id']}...")
                hotel_api._send_request("delete", slot['id'])
                print(f"Hotel slot {slot['id']} cancelled.")
                discrepancies_found = True
                break

    if not discrepancies_found:
        print("\nNo discrepancies found between booked slots.\n")

if __name__ == "__main__":
    # Load configuration and Initialize the API
    config = load_configuration("api.ini")
    hotel_api, band_api = initialize_api(config)

    # Display current reservations
    display_current_slots(hotel_api)
    
    # Checking for errors when maybe 2 hotel slots are reserved and only 1 band slot reserved
    handle_slot_discrepancies(hotel_api, band_api)

    # Check availability of common slots
    common_slots = check_common_slots(hotel_api, band_api)

    # Reserve earliest common slot and release higher slot if necessary
    reserve_earliest_common_slot(hotel_api, band_api, common_slots)

    # Recheck for earlier bookings
    recheck_for_earlier_bookings(hotel_api, band_api)

    # Prompt user for rechecking
    recheck = input("Do you want to recheck for earlier bookings? (y/n): ")
    while recheck.lower() == 'y':
        recheck_for_earlier_bookings(hotel_api, band_api)
        recheck = input("Do you want to recheck for earlier bookings? (y/n): ")

    print("Program stopped.")
