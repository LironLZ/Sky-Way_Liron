from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL
DATABASE_URL = "postgresql://postgres:postgres@db:5432/skyway"  # Update with your credentials
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Session local is used for getting a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class to define the structure of the models (tables)
Base = declarative_base()

def create_stored_procedures():
    """Create all stored procedures for the flight system"""
    procedures = [
        """
        CREATE OR REPLACE FUNCTION get_airline_by_username(username_param TEXT)
        RETURNS TABLE (
            airline_id BIGINT,
            airline_name VARCHAR,
            user_id BIGINT,
            username VARCHAR,
            email VARCHAR
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT a.*, u.username, u.email FROM airlines a
            INNER JOIN users u ON a.user_id = u.id
            WHERE u.username = username_param;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        """
        CREATE OR REPLACE FUNCTION get_customer_by_username(username_param TEXT)
        RETURNS TABLE (
            customer_id BIGINT,
            first_name VARCHAR,
            last_name VARCHAR,
            user_id BIGINT,
            username VARCHAR,
            email VARCHAR
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT c.*, u.username, u.email FROM customers c
            INNER JOIN users u ON c.user_id = u.id
            WHERE u.username = username_param;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        """
        CREATE OR REPLACE FUNCTION get_user_by_username(username_param TEXT)
        RETURNS TABLE (
            id BIGINT,
            username VARCHAR,
            email VARCHAR
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM users WHERE username = username_param;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        """
        CREATE OR REPLACE FUNCTION get_flights_by_parameters(
            origin_country_id_param INT,
            destination_country_id_param INT,
            date_param DATE
        )
        RETURNS TABLE (
            flight_id BIGINT,
            airline_id BIGINT,
            origin_country_id INT,
            destination_country_id INT,
            departure_time TIMESTAMP,
            arrival_time TIMESTAMP,
            remaining_tickets INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM flights
            WHERE origin_country_id = origin_country_id_param
            AND destination_country_id = destination_country_id_param
            AND DATE(departure_time) = date_param;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        """
        CREATE OR REPLACE FUNCTION get_flights_by_airline_id(airline_id_param BIGINT)
        RETURNS TABLE (
            flight_id BIGINT,
            airline_id BIGINT,
            origin_country_id INT,
            destination_country_id INT,
            departure_time TIMESTAMP,
            arrival_time TIMESTAMP,
            remaining_tickets INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM flights WHERE airline_id = airline_id_param;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        """
        CREATE OR REPLACE FUNCTION get_arrival_flights(country_id_param INT)
        RETURNS TABLE (
            flight_id BIGINT,
            airline_id BIGINT,
            origin_country_id INT,
            destination_country_id INT,
            departure_time TIMESTAMP,
            arrival_time TIMESTAMP,
            remaining_tickets INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM flights
            WHERE destination_country_id = country_id_param
            AND arrival_time BETWEEN NOW() AND NOW() + INTERVAL '12 hours';
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        """
        CREATE OR REPLACE FUNCTION get_departure_flights(country_id_param INT)
        RETURNS TABLE (
            flight_id BIGINT,
            airline_id BIGINT,
            origin_country_id INT,
            destination_country_id INT,
            departure_time TIMESTAMP,
            arrival_time TIMESTAMP,
            remaining_tickets INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT * FROM flights
            WHERE origin_country_id = country_id_param
            AND departure_time BETWEEN NOW() AND NOW() + INTERVAL '12 hours';
        END;
        $$ LANGUAGE plpgsql;
        """
    ]

    session = SessionLocal()
    try:
        for procedure in procedures:
            session.execute(text(procedure))
            session.commit()
            print(f"Stored procedure created successfully")
    except Exception as e:
        print(f"Error creating stored procedure: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def drop_stored_procedure(procedure_name: str):
    """Drop a specific stored procedure"""
    session = SessionLocal()
    try:
        session.execute(text(f"DROP FUNCTION IF EXISTS {procedure_name} CASCADE"))
        session.commit()
        print(f"Stored procedure {procedure_name} dropped successfully")
    except Exception as e:
        print(f"Error dropping stored procedure: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def recreate_all_procedures():
    """Drop all procedures and recreate them"""
    procedures_to_drop = [
        'get_airline_by_username(text)',
        'get_customer_by_username(text)',
        'get_user_by_username(text)',
        'get_flights_by_parameters(integer,integer,date)',
        'get_flights_by_airline_id(bigint)',
        'get_arrival_flights(integer)',
        'get_departure_flights(integer)'
    ]
    
    for proc in procedures_to_drop:
        drop_stored_procedure(proc)
    
    create_stored_procedures()

def setup_database():
    """Initialize the database and create stored procedures"""
    try:
        # Create stored procedures
        create_stored_procedures()
        print("Database setup completed successfully")
    except Exception as e:
        print(f"Error during database setup: {e}")