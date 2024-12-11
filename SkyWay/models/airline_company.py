from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, select
from sqlalchemy.orm import relationship
from database.database import Base, SessionLocal

class AirlineCompany(Base):
    __tablename__ = "airline_companies"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False)

    # Relationship to the Flight table
    flights = relationship("Flight", back_populates="airline_company")
    # Relationship to the User table
    user = relationship("User", back_populates="airline_company")

    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(AirlineCompany)
            # Execute the query
            result = session.execute(stmt)
            # Fetch all airlines
            return result.scalars().all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(id):
        session = SessionLocal()
        try:
            return session.get(AirlineCompany, id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        name = itemToAdd.get('name')
        country_id =itemToAdd.get('country_id')
        user_id =itemToAdd.get('user_id')

        try:
            # Create a new item object
            airline_company = AirlineCompany(name=name, country_id=country_id,user_id=user_id)
            # Add the item to the session
            session.add(airline_company)
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
        airline_companies = [AirlineCompany(**item_data) for item_data in listOfItems]
        try:
            # Add all items at once
            session.add_all(airline_companies)
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
            airline_company = AirlineCompany.get_by_id(id).to_dict()  # Fetch the item by id
            if not airline_company:
                return None  # Or raise an exception if the item not found
            # Step 2: Create a new item object with the updated data
            # Ensure the id remains the same
            new_item = AirlineCompany(**updatedItem)
            new_item.id = airline_company.get('id')  # Keep the original ID of the user
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
            stmt = select(AirlineCompany).filter(AirlineCompany.id == id)
            airline_company = session.execute(stmt).scalars().first()
            if not airline_company:
                return None  # item not found
            # Step 2: Delete the item
            session.delete(airline_company)
            # Step 3: Commit the transaction
            session.commit()
            return airline_company  # Return the deleted item or a success response
        finally:
            session.close()

    @staticmethod
    def get_by_country_id(country_id):
        session = SessionLocal()
        try:
            stmt = select(AirlineCompany).where(AirlineCompany.country_id == country_id)
            result = session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            print(f"{e}")
            raise
        finally:
            session.close()


    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "country_id":self.country_id,
            "user_id":self.user_id
        }
