""" Reservation API wrapper

This class implements a simple wrapper around the reservation API. It
provides automatic retries for server-side errors, delays to prevent
server overloading, and produces sensible exceptions for the different
types of client-side error that can be encountered.
"""

# This file contains areas that need to be filled in with your own
# implementation code. They are marked with "Your code goes here".
# Comments are included to provide hints about what you should do.

import requests
import simplejson
import warnings
import time

from requests.exceptions import HTTPError
from exceptions import (
    BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError,
    SlotUnavailableError,ReservationLimitError, MaxRetriesExhaustedError)

class ReservationApi:
    def __init__(self, base_url: str, token: str, retries: int, delay: float):
        """ Create a new ReservationApi to communicate with a reservation
        server.

        Args:
            base_url: The URL of the reservation API to communicate with.
            token: The user's API token obtained from the control panel.
            retries: The maximum number of attempts to make for each request.
            delay: A delay to apply to each request to prevent server overload.
        """
        self.base_url = base_url
        self.token    = token
        self.retries  = retries
        self.delay    = delay

    def _reason(self, req: requests.Response) -> str:
        """Obtain the reason associated with a response"""
        reason = ''

        # Try to get the JSON content, if possible, as that may contain a
        # more useful message than the status line reason
        try:
            json = req.json()
            reason = json['message']

        # A problem occurred while parsing the body - possibly no message
        # in the body (which can happen if the API really does 500,
        # rather than generating a "fake" 500), so fall back on the HTTP
        # status line reason
        except simplejson.errors.JSONDecodeError:
            if isinstance(req.reason, bytes):
                try:
                    reason = req.reason.decode('utf-8')
                except UnicodeDecodeError:
                    reason = req.reason.decode('iso-8859-1')
            else:
                reason = req.reason

        return reason


    def _headers(self) -> dict:
        """Create the authorization token header needed for API requests"""
        # Your code goes here
        return {"Authorization" : f"Bearer {self.token}"}
    

    def _send_request(self, method: str, endpoint: str) -> dict:
        """Send a request to the reservation API and convert errors to
           appropriate exceptions"""
        tries = 0
        while tries < self.retries + 1:
            try:
                tries += 1
                if method == "getHold":
                    result = self.get_slots_held()
                elif method == "getAvailable":
                    result = self.get_slots_available()
                elif method == "postHold":
                    result = self.reserve_slot(endpoint)
                elif method == "delete":
                    result = self.release_slot(endpoint)
                else:
                    raise ValueError(f"Invalid method: {method}")

                time.sleep(self.delay)
                result.raise_for_status()
                return result.json()

            except HTTPError as e:
                if 500 <= result.status_code <= 599:
                    print(f"Server Side Error. Retrying after delay... // Try Number: {tries}")
                    time.sleep(self.delay)
                elif 500 > result.status_code >= 400:
                    self._handle_error(e)
                else:
                    print(f"Unknown error ({result.status_code}): {self._reason(result)}")
                    exit()
        
        raise MaxRetriesExhaustedError("Maximum retries limit reached. Unable to complete the request.")

    def _handle_error(self, error):
        """Handle different types of errors"""
        error_status = error.response.status_code

        if error_status == 400:
            print("Bad Request")
        elif error_status == 401:
            print("The API token was invalid or missing.")
        elif error_status == 403:
            print("SlotId does not exist.")
        elif error_status == 404:
            print("The request has not been processed.")
        elif error_status == 409:
            print("Slot is no longer available.")
        elif error_status == 451:
            print("The client already holds the maximum number of reservations.")
        else:
            print("Unknown error occurred")

        time.sleep(self.delay)
        exit()

    def get_slots_available(self):
        """Obtain the list of slots currently available in the system"""
        # Your code goes here
        headers = self._headers()
        return requests.get(f"{self.base_url}/reservation/available", headers = headers)

    def get_slots_held(self):
        """Obtain the list of slots currently held by the client"""
        # Your code goes here
        headers = self._headers()
        return requests.get(f"{self.base_url}/reservation", headers = headers)

    def release_slot(self, slot_id):
        """Release a slot currently held by the client"""
        # Your code goes here
        headers = self._headers()
        return requests.delete(f"{self.base_url}/reservation/{slot_id}", headers = headers)
            
    def reserve_slot(self, slot_id):
        """Attempt to reserve a slot for the client"""
        # Your code goes here
        headers = self._headers()
        return requests.post(f"{self.base_url}/reservation/{slot_id}", headers = headers)