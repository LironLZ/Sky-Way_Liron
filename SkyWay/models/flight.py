from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey,select, func
from sqlalchemy.orm import relationship
from database.database import Base, SessionLocal
from datetime import datetime

class Flight(Base):
    __tablename__ = "flights"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger, ForeignKey("airline_companies.id"), nullable=False)
    origin_country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    destination_country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    landing_time = Column(DateTime, nullable=False)
    remaining_tickets = Column(Integer, nullable=False)

    # Relationships to Country table
    origin_country = relationship("Country", foreign_keys=[origin_country_id], back_populates="origin_flights")
    destination_country = relationship("Country", foreign_keys=[destination_country_id], back_populates="destination_flights")

    # Relationship to AirlineCompany table
    airline_company = relationship("AirlineCompany", back_populates="flights")


    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(Flight)
            # Execute the query
            result = session.execute(stmt)
            # Fetch all customers
            return result.scalars().all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(id):
        session = SessionLocal()
        try:
            return session.get(Flight, id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        airline_company_id = itemToAdd.get("airline_company_id")
        origin_country_id = itemToAdd.get("origin_country_id")
        destination_country_id = itemToAdd.get("destination_country_id")
        departure_time = itemToAdd.get("departure_time")
        landing_time = itemToAdd.get("landing_time")
        remaining_tickets = itemToAdd.get("remaining_tickets")

        try:
            # Create a new item object
            flight = Flight(airline_company_id=airline_company_id,
                            origin_country_id = origin_country_id,
                            destination_country_id = destination_country_id,
                            departure_time = departure_time,
                            landing_time = landing_time,
                            remaining_tickets = remaining_tickets)

            # Add the item to the session
            session.add(flight)
            # Commit the transaction
            session.commit()
        except Exception as e:
            # If an error occurs, rollback the session
            session.rollback()
            print(f"Error: {e}")
            raise
        finally:
            # Close the session
            session.close()

    @staticmethod
    def add_all(listOfItems):
        session = SessionLocal()
        # Convert the list of dictionaries into the proper objects
        flights = [Flight(**item_data) for item_data in listOfItems]
        try:
            # Add all items at once
            session.add_all(flights)
            # Commit the transaction
            session.commit()
        except Exception as e:
            session.rollback()  # Rollback in case of error
            raise e
        finally:
            session.close()

    @staticmethod
    def update(id, updatedItem):
        session = SessionLocal()
        try:
            # Step 1: Get the item by id
            flight = Flight.get_by_id(id).to_dict()  # Fetch the item by id
            if not flight:
                return None  # Or raise an exception if the item not found
            # Step 2: Create a new item object with the updated data
            # Ensure the id remains the same
            new_item = Flight(**updatedItem)
            new_item.id = flight.get('id')  # Keep the original ID of the user
            # Step 3: Replace the old item object with the new one
            session.merge(new_item)  # `merge` will update the existing record
            session.commit()
            return new_item  # Return the updated item

        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error updating user: {e}")
            return None  # Or handle the exception as needed

        finally:
            session.close()

    @staticmethod
    def remove(id):
        session = SessionLocal()
        try:
            # Step 1: Use select() to fetch the item by id
            stmt = select(Flight).filter(Flight.id == id)
            flight = session.execute(stmt).scalars().first()
            if not flight:
                return None  # item not found
            # Step 2: Delete the item
            session.delete(flight)
            # Step 3: Commit the transaction
            session.commit()
            return flight  # Return the deleted item or a success response
        finally:
            session.close()

    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id" : self.id,
            "airline_company_id" : self.airline_company_id,
            "origin_country_id" :self.origin_country_id,
            "destination_country_id" : self.destination_country_id,
            "departure_time" : self.departure_time,
            "landing_time" : self.landing_time,
            "remaining_tickets" : self.remaining_tickets
        }


def get_by_origin_country(country_id):
    session = SessionLocal()
    try:
        stmt = select(Flight).where(Flight.origin_country_id == country_id)
        result = session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"{e}")
        raise
    finally:
        session.close()

def get_by_destination_country(country_id):
    session = SessionLocal()
    try:
        stmt = select(Flight).where(Flight.destination_country_id == country_id)
        result = session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"{e}")
        raise
    finally:
        session.close()

def get_by_departure_date(date):
    session = SessionLocal()
    try:
        # Convert the incoming date string to a date object
        target_date = datetime.fromisoformat(date).date()

        # Query flights and filter by date
        stmt = select(Flight).where(func.date(Flight.departure_time) == target_date)
        result = session.execute(stmt)
        flights = result.scalars().all()

        return flights
    except Exception as e:
        print(f"{e}")
        raise
    finally:
        session.close()

def get_by_landing_date(date):
    session = SessionLocal()
    try:
        # Convert the incoming date string to a date object
        target_date = datetime.fromisoformat(date).date()

        # Query flights and filter by date
        stmt = select(Flight).where(func.date(Flight.landing_time) == target_date)
        result = session.execute(stmt)
        flights = result.scalars().all()

        return flights
    except Exception as e:
        print(f"{e}")
        raise
    finally:
        session.close()


