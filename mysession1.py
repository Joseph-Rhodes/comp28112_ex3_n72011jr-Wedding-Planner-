# mysession1.py

from reservationapi import ReservationApi
import configparser

# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")


# API keys
band_api_key = "7ad6349ed72b87725b4cdcb335caa08f79ab8378fd73e6104a241d68dbf28a7e"
hotel_api_key = "1a8009a7266545e1bed7d000a74cee31273eee63b09be8bc9015c773ed837100"

# Base URLs for the band and hotel APIs
band_base_url = "https://web.cs.manchester.ac.uk/band/api"
hotel_base_url = "https://web.cs.manchester.ac.uk/hotel/api"

# Number of retries for each request
retries = 3

# Delay (in seconds) between retries
delay = 1

def main():
    # Create instances of ReservationApi for band and hotel
    band_api = ReservationApi(band_base_url, band_api_key, retries, delay)
    hotel_api = ReservationApi(hotel_base_url, hotel_api_key, retries, delay)

    # Task 3.1: Check for free slots
    print("Checking for free slots:")
    available_slots_band = band_api.get_slots_available()
    available_slots_hotel = hotel_api.get_slots_available()
    print("Available slots in the band:", available_slots_band)
    print("Available slots in the hotel:", available_slots_hotel)

    # Task 3.2: Reserve a slot
    print("\nReserving a slot:")
    slot_to_reserve = 546  # Change slot ID as needed
    band_reservation_response = band_api.reserve_slot(slot_to_reserve)
    print("Band reservation response:", band_reservation_response)
    hotel_reservation_response = hotel_api.reserve_slot(slot_to_reserve)
    print("Hotel reservation response:", hotel_reservation_response)
    

    # Task 3.4: Get slots held
    print("\nRetrieving held slots:")
    held_slots_band = band_api.get_slots_held()
    print("Held slots in the band:", held_slots_band)

    held_slots_hotel = hotel_api.get_slots_held()
    print("Held slots in the hotel:", held_slots_hotel)

    # Task 3.3: Cancel a reservation
    print("\nCancelling a reservation:")
    slot_to_cancel = 570  # Change slot ID as needed
    band_api.release_slot(slot_to_cancel)
    hotel_api.release_slot(slot_to_cancel)
    


if __name__ == "__main__":
    main()
