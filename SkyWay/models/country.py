from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import relationship
from database.database import Base, SessionLocal

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationships to the Flight table
    origin_flights = relationship("Flight", foreign_keys="[Flight.origin_country_id]", back_populates="origin_country")
    destination_flights = relationship("Flight", foreign_keys="[Flight.destination_country_id]", back_populates="destination_country")

    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(Country)
            # Execute the query
            result = session.execute(stmt)
            # Fetch all countries
            return result.scalars().all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(id):
        session = SessionLocal()
        try:
            return session.get(Country, id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        name = itemToAdd.get('name')

        try:
            # Create a new item object
            country = Country(name=name)
            # Add the object to the session
            session.add(country)
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
        countries = [Country(**item_data) for item_data in listOfItems]
        try:
            # Add all items at once
            session.add_all(countries)
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
            country = Country.get_by_id(id).to_dict()  # Fetch the item by id
            if not country:
                return None  # Or raise an exception if item not found
            # Step 2: Create a new item object with the updated data
            # Ensure the ID remains the same
            new_item = Country(**updatedItem)
            new_item.id = country.get('id')  # Keep the original id of the item
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
            stmt = select(Country).filter(Country.id == id)
            country = session.execute(stmt).scalars().first()
            if not country:
                return None  # item not found
            # Step 2: Delete the item
            session.delete(country)
            # Step 3: Commit the transaction
            session.commit()
            return country  # Return the deleted item or a success response
        finally:
            session.close()

    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name
        }