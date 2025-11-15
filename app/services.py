from common import *
import requests


# ==============================================
# FLIGHTS SERVICE CLIENT
# ==============================================

class FlightsService:
    def __init__(self, base_url):
        self.base_url = base_url

    def health_check(self):
        response = requests.get(f"{self.base_url}/manage/health")
        response.raise_for_status()

    def get_all_flights(self, page: int = None, size: int = None):
        query_params = {"page": page, "size": size}
        response = requests.get(f"{self.base_url}/flights", params=query_params)
        response.raise_for_status()
        return PaginationResponse.model_validate(response.json())

    def get_flight_by_number(self, flight_number: str) -> FlightResponse:
        response = requests.get(f"{self.base_url}/flights/{flight_number}")
        response.raise_for_status()
        return FlightResponse.model_validate(response.json())


# ==============================================
# TICKETS SERVICE CLIENT
# ==============================================

class TicketsService:
    def __init__(self, base_url):
        self.base_url = base_url

    def health_check(self):
        response = requests.get(f"{self.base_url}/manage/health")
        response.raise_for_status()

    def get_user_tickets(self, username: str) -> list[Ticket]:
        response = requests.get(f"{self.base_url}/tickets/user/{username}")
        response.raise_for_status()
        return [Ticket.model_validate(item) for item in response.json()]

    def get_ticket_by_uid(self, ticket_uid: uuid.UUID) -> Ticket | None:
        response = requests.get(f"{self.base_url}/tickets/{ticket_uid}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return Ticket.model_validate(response.json())

    def remove_ticket(self, ticket_uid: uuid.UUID) -> None:
        response = requests.delete(f"{self.base_url}/tickets/{ticket_uid}")
        response.raise_for_status()

    def create_new_ticket(self, ticket_uid: uuid.UUID, username: str, flight_number: str, price: int):
        ticket_data = TicketCreateRequest(
            ticketUid=ticket_uid,
            username=username,
            flightNumber=flight_number,
            price=price,
        )
        response = requests.post(
            f"{self.base_url}/tickets",
            json=ticket_data.model_dump(mode="json")
        )
        response.raise_for_status()


# ==============================================
# PRIVILEGES SERVICE CLIENT
# ==============================================

class PrivilegesService:
    def __init__(self, base_url):
        self.base_url = base_url

    def health_check(self):
        response = requests.get(f"{self.base_url}/manage/health")
        response.raise_for_status()

    def get_user_privilege(self, username: str) -> Privilege | None:
        response = requests.get(f"{self.base_url}/privilege/{username}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return Privilege.model_validate(response.json())

    def get_user_privilege_history(self, username: str) -> list[PrivilegeHistory]:
        response = requests.get(f"{self.base_url}/privilege/{username}/history")
        response.raise_for_status()
        return [PrivilegeHistory.model_validate(item) for item in response.json()]

    def get_user_privilege_transaction(self, username: str, ticket_uid: uuid.UUID) -> PrivilegeHistory | None:
        response = requests.get(f"{self.base_url}/privilege/{username}/history/{ticket_uid}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return PrivilegeHistory.model_validate(response.json())

    def add_privilege_transaction(self, username: str, transaction_data: AddTranscationRequest):
        response = requests.post(
            f"{self.base_url}/privilege/{username}/history",
            json=transaction_data.model_dump(mode="json")
        )
        response.raise_for_status()

    def revert_transaction(self, username: str, ticket_uid: uuid.UUID):
        response = requests.delete(
            f"{self.base_url}/privilege/{username}/history/{ticket_uid}"
        )
        response.raise_for_status()