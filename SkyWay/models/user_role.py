from sqlalchemy import Column, Integer, String, select
from database.database import Base, SessionLocal

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, unique=True)


    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(UserRole)
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
            return session.get(UserRole, id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        role_name = itemToAdd.get('role_name')

        try:
            # Create a new item object
            user_role = UserRole(role_name=role_name)
            # Add the object to the session
            session.add(user_role)
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
        user_roles = [UserRole(**item_data) for item_data in listOfItems]
        try:
            # Add all items at once
            session.add_all(user_roles)
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
            user_role = UserRole.get_by_id(id).to_dict()  # Fetch the item by id
            if not user_role:
                return None  # Or raise an exception if item not found
            # Step 2: Create a new item object with the updated data
            # Ensure the ID remains the same
            new_item = UserRole(**updatedItem)
            new_item.id = user_role.get('id')  # Keep the original id of the item
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
            stmt = select(UserRole).filter(UserRole.id == id)
            user_role = session.execute(stmt).scalars().first()
            if not user_role:
                return None  # item not found
            # Step 2: Delete the item
            session.delete(user_role)
            # Step 3: Commit the transaction
            session.commit()
            return user_role  # Return the deleted item or a success response
        finally:
            session.close()

    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id": self.id,
            "role_name": self.role_name
        }