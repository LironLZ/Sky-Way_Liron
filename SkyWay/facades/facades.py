from datetime import datetime
from business_logic.login_token import LoginToken
from database.repository import getFlightsByCustomer
from models.airline_company import AirlineCompany
from models.country import Country
from models.customer import Customer
from models.ticket import Ticket
from models.user import User
from sqlalchemy import text
from typing import List, Dict, Optional
from abc import ABC
from database.database import Base, SessionLocal

from models.flight import Flight, get_by_destination_country, get_by_origin_country

class FacadeBase(ABC):
    """Base facade class that defines common interface for all facades"""
    
    def get_all_flights(self) -> List[Dict]:
        """Get all available flights"""
        pass
    
    def get_flight_by_id(self, flight_id: int) -> Optional[Dict]:
        """Get flight by ID"""
        pass
    
    def get_flights_by_parameters(self, origin_country_id: int, 
                                destination_country_id: int, 
                                date: datetime) -> List[Dict]:
        """Get flights by search parameters"""
        pass
    
    def get_all_airlines(self) -> List[Dict]:
        """Get all airlines"""
        pass
    
    def get_airline_by_id(self, airline_id: int) -> Optional[Dict]:
        """Get airline by ID"""
        pass
    
    def get_airline_by_parameters(self, **params) -> List[Dict]:
        """Get airlines by parameters"""
        pass
    
    def get_all_countries(self) -> List[Dict]:
        """Get all countries"""
        pass
    
    def get_country_by_id(self, country_id: int) -> Optional[Dict]:
        """Get country by ID"""
        pass
    
    def create_new_user(self, user: Dict) -> Dict:
        """Create new user (internal usage)"""
        pass

class AnonymousFacade(FacadeBase):
    """Facade for anonymous users with limited access"""
    def __init__(self, login_token: Optional[LoginToken] = None):
        self.login_token = login_token

    def validate_user_role(self, required_role: str) -> bool:
        """Validate that the user has the required role"""
        if not self.login_token:
            return False
        return self.login_token.role.lower() == required_role.lower()

    def get_all_flights(self) -> List[Dict]:
        """Implementation of get all flights"""
        
        return Flight.get_all()
    
    def get_flight_by_id(self, flight_id: int) -> Optional[Dict]:
        """Implementation of get flight by ID"""
        return Flight.get_by_id(flight_id)
    
    def get_flights_by_parameters(self, origin_country_id: int, 
                                destination_country_id: int, 
                                date: datetime) -> List[Dict]:
        """Implementation of get flights by parameters"""
        session = SessionLocal()
        try:
            result = session.execute(
                text("SELECT * FROM get_flights_by_parameters(:origin, :destination, :date)"),
                {"origin": origin_country_id, "destination": destination_country_id, "date": date}
            )
            return result.fetchall()
        finally:
            session.close()

    
    def get_all_airlines(self) -> List[Dict]:
        """Implementation of get all airlines"""
        return AirlineCompany.get_all()
    
    def get_airline_by_id(self, airline_id: int) -> Optional[Dict]:
        """Implementation of get airline by ID"""
        return AirlineCompany.get_by_id(airline_id)
    
    def get_airline_by_parameters(self, **params) -> List[Dict]:
        """Implementation of get airlines by parameters"""
        filtered_airlines = self.get_all_airlines()
        for key, value in params.items():
            filtered_airlines = [
                airline for airline in filtered_airlines 
                if airline.get(key) == value
            ]
        return filtered_airlines
    
    def get_all_countries(self) -> List[Dict]:
        """Implementation of get all countries"""
        return Country.get_all()
    
    def get_country_by_id(self, country_id: int) -> Optional[Dict]:
        """Implementation of get country by ID"""
        return Country.get_by_id(country_id)
    
    def login(self, username: str, password: str) -> bool:
        """Login method for anonymous users"""
        # Implement login logic here
        pass
    
    def create_new_user(self, user: Dict) -> Dict:
        """Create new user (internal usage)"""
        return User.add(user)

    def add_customer(self, customer: Dict) -> Dict:
        """Add a new customer"""
        Customer.add(customer)

class CustomerFacade(AnonymousFacade):
    """Facade for registered customers"""
    
    def update_customer(self, customer_data: Dict) -> bool:
        """Update customer details"""
        Customer.update(customer_data)
    
    def add_ticket(self, flight_id: int) -> bool:
        """Purchase a ticket for a flight"""
        ticket = {"flight_id": flight_id,
                  "customer_id": self.customer_id}
        Ticket.add(ticket)
    
    def remove_ticket(self, ticket_id: int) -> bool:
        """Remove/cancel a purchased ticket"""
        Ticket.remove(ticket_id)
    
    def get_my_tickets(self) -> List[Dict]:
        """Get all tickets for the current customer"""
        return getFlightsByCustomer(self.customer_id)

class AirlineFacade(AnonymousFacade):
    """Facade for airline companies"""
    
    def update_airline(self, airline_data: Dict) -> bool:
        """Update airline details"""
        pass
    
    def update_flight(self, flight_data: Dict) -> bool:
        """Update flight details"""
        pass
    
    def remove_flight(self, flight_id: int) -> bool:
        """Remove a flight"""
        pass
    
    def get_my_flights(self) -> List[Dict]:
        """Get all flights for the current airline"""
        pass

class AdministratorFacade(AnonymousFacade):
    """Facade for system administrators"""
    
    def get_all_customers(self) -> List[Dict]:
        """Get all registered customers"""
        pass
    
    def add_airline(self, airline_data: Dict) -> bool:
        """Add a new airline"""
        pass
    
    def add_administrator(self, admin_data: Dict) -> bool:
        """Add a new administrator"""
        pass
    
    def remove_airline(self, airline_id: int) -> bool:
        """Remove an airline"""
        pass
    
    def remove_customer(self, customer_id: int) -> bool:
        """Remove a customer"""
        pass
    
    def remove_administrator(self, admin_id: int) -> bool:
        """Remove an administrator"""
        pass