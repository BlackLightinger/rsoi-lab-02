import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime
from enum import Enum


# ==============================================
# DATABASE ENTITY MODELS
# ==============================================

class Ticket(BaseModel):
    id: int
    ticket_uid: uuid.UUID
    username: str
    flight_number: str
    price: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class Flight(BaseModel):
    id: int
    flight_number: str
    datetime: datetime
    from_airport_id: int
    to_airport_id: int
    price: int

    model_config = ConfigDict(from_attributes=True)


class Airport(BaseModel):
    id: int
    name: str
    city: str
    country: str

    model_config = ConfigDict(from_attributes=True)


class Privilege(BaseModel):
    id: int
    username: str
    status: str
    balance: int

    model_config = ConfigDict(from_attributes=True)


class PrivilegeHistory(BaseModel):
    id: int
    privilege_id: int
    ticket_uid: uuid.UUID
    datetime: datetime
    balance_diff: int
    operation_type: str

    model_config = ConfigDict(from_attributes=True)


# ==============================================
# ENUMERATION TYPES
# ==============================================

class TicketStatus(str, Enum):
    PAID = "PAID"
    CANCELED = "CANCELED"


class PrivilegeStatus(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"


class OperationType(str, Enum):
    FILL_IN_BALANCE = "FILL_IN_BALANCE"
    DEBIT_THE_ACCOUNT = "DEBIT_THE_ACCOUNT"


# ==============================================
# FLIGHT RELATED MODELS
# ==============================================

class FlightResponse(BaseModel):
    flightNumber: str = Field(..., description="Flight number")
    fromAirport: str = Field(..., description="Departure airport and city")
    toAirport: str = Field(..., description="Arrival airport and city")
    date: datetime = Field(..., description="Departure date and time in ISO 8601")
    price: int = Field(..., description="Ticket price")

    model_config = ConfigDict(from_attributes=True)


class PaginationResponse(BaseModel):
    page: int = Field(..., description="Current page number")
    pageSize: int = Field(..., description="Number of items per page")
    totalElements: int = Field(..., description="Total number of items")
    items: List[FlightResponse] = Field(..., description="List of flights")

    model_config = ConfigDict(from_attributes=True)


# ==============================================
# TICKET RELATED MODELS
# ==============================================

class TicketResponse(BaseModel):
    ticketUid: uuid.UUID = Field(..., description="Unique ticket identifier")
    flightNumber: str = Field(..., description="Flight number")
    fromAirport: str = Field(..., description="Departure airport")
    toAirport: str = Field(..., description="Arrival airport")
    date: datetime = Field(..., description="Flight date and time")
    price: int = Field(..., description="Ticket price")
    status: TicketStatus = Field(..., description="Current ticket status")

    model_config = ConfigDict(from_attributes=True)


class TicketPurchaseRequest(BaseModel):
    flightNumber: str = Field(..., description="Flight number to book")
    price: int = Field(..., description="Ticket price")
    paidFromBalance: bool = Field(
        ..., description="Use bonus points for payment"
    )


class TicketPurchaseResponse(BaseModel):
    ticketUid: uuid.UUID = Field(..., description="Created ticket UUID")
    flightNumber: str = Field(..., description="Booked flight number")
    fromAirport: str = Field(..., description="Departure airport details")
    toAirport: str = Field(..., description="Arrival airport details")
    date: datetime = Field(..., description="Scheduled departure time")
    price: int = Field(..., description="Total ticket price")
    paidByMoney: int = Field(..., description="Amount paid with money")
    paidByBonuses: int = Field(..., description="Amount paid with bonus points")
    status: TicketStatus = Field(..., description="Booking status")
    privilege: "PrivilegeShortInfo" = Field(
        ..., description="Loyalty program information"
    )


class TicketCreateRequest(BaseModel):
    ticketUid: uuid.UUID = Field(..., description="Unique ticket identifier")
    username: str = Field(..., description="Ticket owner username")
    flightNumber: str = Field(..., description="Associated flight number")
    price: int = Field(..., description="Ticket price")


# ==============================================
# PRIVILEGE AND LOYALTY MODELS
# ==============================================

class PrivilegeShortInfo(BaseModel):
    balance: int = Field(..., description="Available bonus points")
    status: PrivilegeStatus = Field(..., description="Current loyalty tier")

    model_config = ConfigDict(from_attributes=True)


class BalanceHistory(BaseModel):
    date: datetime = Field(..., description="Transaction timestamp")
    ticketUid: uuid.UUID = Field(
        ..., description="Associated ticket identifier"
    )
    balanceDiff: int = Field(..., description="Points change amount")
    operationType: OperationType = Field(..., description="Transaction type")

    model_config = ConfigDict(from_attributes=True)


class PrivilegeInfoResponse(BaseModel):
    balance: int = Field(..., description="Current points balance")
    status: PrivilegeStatus = Field(..., description="Loyalty program status")
    history: List[BalanceHistory] = Field(
        ..., description="Points transaction history"
    )


class AddTransactionRequest(BaseModel):
    privilege_id: int = Field(..., description="Privilege account ID")
    ticket_uid: uuid.UUID = Field(..., description="Related ticket UUID")
    datetime: datetime = Field(..., description="Transaction timestamp")
    balance_diff: int = Field(..., description="Points change amount")
    operation_type: str = Field(..., description="Type of operation")


# ==============================================
# USER PROFILE MODELS
# ==============================================

class UserInfoResponse(BaseModel):
    tickets: List[TicketResponse] = Field(
        ..., description="User's ticket collection"
    )
    privilege: PrivilegeShortInfo = Field(
        ..., description="Loyalty program details"
    )


# ==============================================
# ERROR HANDLING MODELS
# ==============================================

class ErrorDescription(BaseModel):
    field: str = Field(..., description="Field with validation error")
    error: str = Field(..., description="Error description")


class ErrorResponse(BaseModel):
    message: str = Field(..., description="Error message")


class ValidationErrorResponse(BaseModel):
    message: str = Field(..., description="General error message")
    errors: List[ErrorDescription] = Field(
        ..., description="Detailed field validation errors"
    )