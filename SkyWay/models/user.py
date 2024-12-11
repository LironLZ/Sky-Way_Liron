from requests import session
from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base, SessionLocal
from sqlalchemy import select

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    user_role = Column(Integer, ForeignKey("user_roles.id"), nullable=False)

    # Relationship to AirlineCompany (optional, only if this user is an airline company)
    airline_company = relationship("AirlineCompany", back_populates="user", uselist=False)

    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(User)
            # Execute the query
            result = session.execute(stmt)
            # Fetch all users
            return result.scalars().all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(id):
        session = SessionLocal()
        try:
            return session.get(User,id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        username = itemToAdd.get('username')
        password = itemToAdd.get('password')
        email = itemToAdd.get('email')
        user_role = itemToAdd.get('user_role')

        try:
            # Create a new User object
            user = User(username=username, password=password, email=email, user_role=user_role)
            # Add the object to the session
            session.add(user)
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
        users = [User(**item_data) for item_data in listOfItems]
        try:
            # Add all users at once
            session.add_all(users)
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
            user = User.get_by_id(id).to_dict() # Fetch the user by ID
            if not user:
                return None  # Or raise an exception if user not found
            # Step 2: Create a new User object with the updated data
            # Ensure the ID remains the same
            new_item = User(**updatedItem)
            new_item.id = user.get('id')  # Keep the original ID of the user
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
            stmt = select(User).filter(User.id == id)
            item = session.execute(stmt).scalars().first()
            if not item:
                return None  # User not found
            # Step 2: Delete the user
            session.delete(item)
            # Step 3: Commit the transaction
            session.commit()
            return item  # Return the deleted user or a success response
        finally:
            session.close()

    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password":self.password,
            "user_role":self.user_role
        }