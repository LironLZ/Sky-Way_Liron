from sqlalchemy import Column, BigInteger, String, ForeignKey, select
from database.database import Base, SessionLocal

class Customer(Base):
    __tablename__ = "customers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_no = Column(String, unique=True)
    credit_card_no = Column(String, unique=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True)


    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            stmt = select(Customer)
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
            return session.get(Customer, id)
        finally:
            session.close()

    @staticmethod
    def add(itemToAdd):
        session = SessionLocal()

        first_name = itemToAdd.get('first_name')
        last_name = itemToAdd.get('last_name')
        address = itemToAdd.get('address')
        phone_no = itemToAdd.get('phone_no')
        credit_card_no = itemToAdd.get('credit_card_no')
        user_id = itemToAdd.get('user_id')

        try:
            # Create a new item object
            customer = Customer(first_name=first_name,last_name=last_name,address=address,
                                phone_no=phone_no,credit_card_no=credit_card_no,user_id=user_id)
            # Add the item to the session
            print(f"the customer to add is: {customer}")
            session.add(customer)
            # Commit the transaction
            session.commit()
        except Exception as e:
            # If an error occurs, rollback the session
            session.rollback()
            print(f"ERROR ACCURED HERE, CHECK IT OUT: {e}")
            raise
        finally:
            # Close the session
            session.close()

    @staticmethod
    def add_all(listOfItems):
        session = SessionLocal()
        # Convert the list of dictionaries into the proper objects
        customers = [Customer(**item_data) for item_data in listOfItems]
        try:
            # Add all items at once
            session.add_all(customers)
            # Commit the transaction
            session.commit()
        except Exception as e:
            session.rollback()  # Rollback in case of error
            raise
        finally:
            session.close()

    @staticmethod
    def update(id, updatedItem):
        session = SessionLocal()
        try:
            # Step 1: Get the item by id
            customer = Customer.get_by_id(id).to_dict()  # Fetch the item by id
            if not customer:
                return None  # Or raise an exception if the item not found
            # Step 2: Create a new item object with the updated data
            # Ensure the id remains the same
            new_item = Customer(**updatedItem)
            new_item.id = customer.get('id')  # Keep the original ID of the user
            # Step 3: Replace the old item object with the new one
            session.merge(new_item)  # `merge` will update the existing record
            session.commit()
            return new_item  # Return the updated item

        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error updating user: {e}")
            raise # Or handle the exception as needed

        finally:
            session.close()

    @staticmethod
    def remove(id):
        session = SessionLocal()
        try:
            # Step 1: Use select() to fetch the item by id
            stmt = select(Customer).filter(Customer.id == id)
            customer = session.execute(stmt).scalars().first()
            if not customer:
                return None  # item not found
            # Step 2: Delete the item
            session.delete(customer)
            # Step 3: Commit the transaction
            session.commit()
            return customer  # Return the deleted item or a success response
        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error deleting customer: {e}")
            raise
        finally:
            session.close()

    def to_dict(self):
        """
        Convert the model instance into a dictionary.
        """
        return {
            "id" : self.id,
            "first_name" :self.first_name,
            "last_name" : self.last_name,
            "address" : self.address,
            "phone_no" : self.phone_no,
            "credit_card_no" : self.credit_card_no,
            "user_id" : self.user_id,
        }
