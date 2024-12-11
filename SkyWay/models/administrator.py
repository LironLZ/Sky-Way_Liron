from sqlalchemy import Column, select, String, BigInteger, ForeignKey
from database.database import Base, SessionLocal

class Administrator(Base):
    __tablename__ = "administrators"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False)

    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(Administrator)
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
            return session.get(Administrator, id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        first_name = itemToAdd.get('first_name')
        last_name = itemToAdd.get('last_name')
        user_id = itemToAdd.get('user_id')

        try:
            # Create a new item object
            administrator = Administrator(first_name,last_name,user_id)
            # Add the object to the session
            session.add(administrator)
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
        administrators = [Administrator(**item_data) for item_data in listOfItems]
        try:
            # Add all users at once
            session.add_all(administrators)
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
            # Step 1: Get the user by ID
            administrator = Administrator.get_by_id(id).to_dict()  # Fetch the user by ID
            if not administrator:
                return None  # Or raise an exception if user not found
            # Step 2: Create a new User object with the updated data
            # Ensure the ID remains the same
            new_item = Administrator(**updatedItem)
            new_item.id = administrator.get('id')  # Keep the original ID of the user
            # Step 3: Replace the old user object with the new one
            session.merge(new_item)  # `merge` will update the existing record
            session.commit()
            return new_item  # Return the updated user

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
            # Step 1: Use select() to fetch the user by ID
            stmt = select(Administrator).filter(Administrator.id == id)
            administrator = session.execute(stmt).scalars().first()
            if not administrator:
                return None  # User not found
            # Step 2: Delete the user
            session.delete(administrator)
            # Step 3: Commit the transaction
            session.commit()
            return administrator  # Return the deleted user or a success response
        finally:
            session.close()

    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name":self.last_name,
            "user_id": self.user_id
        }