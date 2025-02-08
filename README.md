# Wedding Planner Reservation System

## Overview
This project is a client-server application developed as part of **COMP28112** coursework at the **University of Manchester**. The objective is to implement a **distributed system** that reserves the same **timeslot** for both a **hotel** and a **band** using **Web Services, HTTP protocol, and JSON markup language**.

The system must handle **concurrent requests, message delays, and failures**, while ensuring that the earliest available matching slots are reserved. The solution is implemented in **Python** and adheres to the constraints provided in the coursework.

---

## Features
- **Session 1: Basic Reservation Operations**
  - Reserve a slot at the hotel or band.
  - Cancel a reservation.
  - Find available slots.
  - Check slots reserved by the user.

- **Session 2: Optimized Slot Booking Strategy**
  - Reserve the earliest available matching slot for both the hotel and the band.
  - Handle errors, delays, and concurrency issues.
  - Implement a **retry mechanism** with a **minimum 1-second delay** between requests.
  - Ensure that unmatched bookings are canceled appropriately.

---

## Technologies Used
- **Python 3**
- **HTTP Requests (using `requests` library)**
- **JSON for API communication**
- **RESTful Web APIs**
- **Swagger API Interface for debugging and testing**

---


## Setting up API Keys
Before running the client, you need to obtain **API keys** for both the hotel and the band.

- Visit [Hotel API](https://web.cs.manchester.ac.uk/hotel/) and log in with your university credentials.
- Visit [Band API](https://web.cs.manchester.ac.uk/band/) and log in.
- Copy and paste the API keys into the `api.ini` configuration file.

---

## Usage

### Running Session 1 (Basic Operations)
```sh
python mysession1.py
```
This will:
- Check available slots.
- Reserve a slot.
- Retrieve reserved slots.
- Cancel a reservation.

### Running Session 2 (Optimized Matching)
```sh
python mysession2.py
```
This will:
- Find common available slots.
- Book the earliest common slot.
- Cancel unnecessary bookings.
- Re-check availability for better slots.

---

## API Reference
The hotel and band reservation services provide **RESTful APIs** with the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/reservation/{slotid}` | `POST` | Reserve a slot |
| `/api/reservation/{slotid}` | `DELETE` | Cancel a reservation |
| `/api/reservation/available` | `GET` | Retrieve available slots |
| `/api/reservation` | `GET` | Retrieve slots booked by the user |

Authentication is required via the **Authorization: Bearer <API Key>** header.

---

## Error Handling
The system gracefully handles API failures with appropriate error codes:
- **200**: Success ✅
- **400**: Bad Request ❌
- **401**: Unauthorized ❌ (Invalid API Key)
- **403**: Forbidden ❌ (Invalid slot ID)
- **409**: Conflict ❌ (Slot already booked)
- **503**: Service Unavailable ❌ (Retry later)

Retries are implemented with an **exponential backoff mechanism** to avoid overwhelming the servers.

---

## License
This project is for educational purposes and follows **University of Manchester's coursework policies**. Do **NOT** share API keys or credentials online.

---

