from requests import session
from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint,select
from database.database import Base, SessionLocal
from models.customer import Customer
from models.flight import Flight

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger, ForeignKey("flights.id"))
    customer_id = Column(BigInteger, ForeignKey("customers.id"))

    # Unique constraint on combination of Flight_Id and Customer_Id
    __table_args__ = (UniqueConstraint("flight_id", "customer_id", name="_flight_customer_uc"),)

    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(Ticket)
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
            return session.get(Ticket, id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        flight_id = itemToAdd.get('flight_id')
        customer_id = itemToAdd.get('customer_id')
        try:
            # Create a new item object
            ticket = Ticket(flight_id=flight_id,customer_id=customer_id)
            # Add the item to the session
            session.add(ticket)
            # Commit the transaction
            session.commit()
        except Exception as e:
            # If an error occurs, rollback the session
            session.rollback()
            print(f"Error: {e}")
        finally:
            # Close the session
            session.close()

    @staticmethod
    def add_all(listOfItems):
        session = SessionLocal()
        # Convert the list of dictionaries into the proper objects
        tickets = [Ticket(**item_data) for item_data in listOfItems]
        try:
            # Add all items at once
            session.add_all(tickets)
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
            ticket = Ticket.get_by_id(id).to_dict()  # Fetch the item by id
            if not ticket:
                return None  # Or raise an exception if the item not found
            # Step 2: Create a new item object with the updated data
            # Ensure the id remains the same
            new_item = Ticket(**updatedItem)
            new_item.id = ticket.get('id')  # Keep the original ID of the user
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
            stmt = select(Ticket).filter(Ticket.id == id)
            ticket = session.execute(stmt).scalars().first()
            if not ticket:
                return None  # item not found
            # Step 2: Delete the item
            session.delete(ticket)
            # Step 3: Commit the transaction
            session.commit()
            return ticket  # Return the deleted item or a success response
        finally:
            session.close()

    def get_all_flights_by_customer(customer):
        flights = []
        session = SessionLocal()

        try:
            # Find the customer by user_id
            target_customer_stmt = select(Customer).where(Customer.user_id == customer.get('user_id'))
            target_customer = session.execute(target_customer_stmt).scalars().first()

            if not target_customer:
                raise ValueError(f"No customer found with user_id: {customer.get('user_id')}")

            target_customer_id = target_customer.id

            # Fetch all flights for the customer's tickets in one query
            flight_stmt = (
                select(Flight)
                .join(Ticket, Flight.id == Ticket.flight_id)
                .where(Ticket.customer_id == target_customer_id)
            )
            flights = session.execute(flight_stmt).scalars().all()

        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error finding flights of customer: {customer.get('user_id')}")
            raise
        finally:
            session.close()

        return [flight.to_dict() for flight in flights]

    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id" : self.id,
            "flight_id" : self.flight_id,
            "customer_id" : self.customer_id
        }

