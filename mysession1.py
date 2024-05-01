import reservationapi
import configparser

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
    return hotel

# Your code goes here
def reserve_slot(api, slot_id):
    """Reserve a slot."""
    print(f"Attempting to reserve slot {slot_id}:\n")
    print(api._send_request("postHold", slot_id))

def delete_reservation(api, reservation_id):
    """Delete a reservation."""
    print(f"\nAttempting to delete slot {reservation_id}:\n")
    print(api._send_request("delete", reservation_id))

def check_available(api, parameters):
    """Check availability."""
    print("\nChecking available slots:\n")
    print(api._send_request("getAvailable", parameters))

def check_reserved_slots(api, user_id):
    """Check slots reserved by a user."""
    print("\nSlot reserved by you:\n")
    print(api._send_request("getHold", user_id))

if __name__ == "__main__":
    # Load configuration and Initialize the API
    config = load_configuration("api.ini")
    hotel_api = initialize_api(config)
    
    # Example usage
    reserve_slot(hotel_api, "546")
    check_reserved_slots(hotel_api, "0")
    delete_reservation(hotel_api, "546")
    check_reserved_slots(hotel_api, "0")
    check_available(hotel_api,"0")