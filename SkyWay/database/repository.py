from csv import excel

from flask import Blueprint, request,jsonify
from database.database import engine
from sqlalchemy import text

from models.administrator import Administrator
from models.airline_company import AirlineCompany
from models.country import Country
from models.customer import Customer
from models.ticket import Ticket
from models.user import User
from models.flight import  Flight
from models.user_role import UserRole

repo_blueprint = Blueprint('repo_blueprint', __name__)


# Map table names to models
MODEL_MAP = {
    "user": User,
    "flight": Flight,
    "country": Country,
    "ticket": Ticket,
    "administrator":Administrator,
    "airline_company": AirlineCompany,
    'customer': Customer,
    "user_role": UserRole
}

@repo_blueprint.route('/<string:table>/<int:item_id>', methods=['GET'])
def get_by_id(table,item_id):
    model = MODEL_MAP.get(table)
    if not model:
        return jsonify({"error": f"No table found for {table}"}), 404

    item = model.get_by_id(item_id)
    if not item:
        return jsonify({"error": f"No {table} found with ID {item_id}"}), 404

    return jsonify(item.to_dict())  # Assuming `to_dict` exists on the model

@repo_blueprint.route('/<string:table>', methods=['GET'])
def get_all(table):
    model = MODEL_MAP.get(table)
    airlineByUsername = get_airline_by_username('ELAL')
    print(airlineByUsername)
    if not model:
        return jsonify({"error": f"No table found for {table}"}), 404
    result = model.get_all()  # If the model is found, call the get_all method
    if result:
        return jsonify([item.to_dict() for item in result])  # Assuming `to_dict` method exists
    else:
        return jsonify({"error": f"No records found for {table}"}), 404

@repo_blueprint.route('/<string:table>/add', methods=['POST'])
def add(table):
    model = MODEL_MAP.get(table)
    if not model:
        return jsonify({"error": f"No table found for {table}"}), 404
    if not request.json:
        return jsonify({"error": f"No content to add to {table}"}), 202
    try:
        model.add(request.json)
    except Exception as e:
        return f"{e}", 400
    return f"{request.json} has been added successfully",201

@repo_blueprint.route('/<string:table>/addAll', methods=['POST'])
def add_all(table):
    model = MODEL_MAP.get(table)
    if not model:
        return jsonify({"error": f"No table found for {table}"}), 404
    if not request.json:
        return jsonify({"error": f"No content to add to {table}"}), 202
    model.add_all(request.json)
    return f"{request.json} has been added successfully",201

@repo_blueprint.route('/<string:table>/update/<int:item_id>', methods=['PUT'])
def update(table,item_id):
    model = MODEL_MAP.get(table)
    if not model:
        return jsonify({"error": f"No table found for {table}"}), 404
    if not request.json:
        return jsonify({"error": f"No content to update to {table}"}), 202
    result = model.update(item_id,request.json)
    if not result:
        return jsonify({"error": "Item not found"}), 404
    return f"{request.json} has been updated successfully", 200

@repo_blueprint.route('/<string:table>/<int:item_id>', methods=['DELETE'])
def remove(table,item_id):
    model = MODEL_MAP.get(table)
    if not model:
        return jsonify({"error": f"No table found for {table}"}), 404
    item = model.remove(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict())



def getAirlinesByCountry(country_id):
    try:
        return AirlineCompany.get_by_country_id(country_id)
    except Exception as e:
        return f"{e}"

def getFlightsByOriginCountry(country_id):
    try:
        return Flight.get_by_origin_country(country_id)
    except Exception as e:
        return f"{e}"

def getFlightsByDestionationCountryId(country_id):
    try:
        return Flight.get_by_destination_country(country_id)
    except Exception as e:
        return f"{e}"

def getFlightsByDepartureDate(date):
    try:
        return Flight.get_by_departure_date(date)
    except Exception as e:
        return f"{e}"

def getFlightsByLandingDate(date):
    try:
        return Flight.get_by_landing_date(date)
    except Exception as e:
        return f"{e}"


def getFlightsByCustomer(customer):
    try:
        return Ticket.get_all_flights_by_customer(customer)
    except Exception as e:
        return f"{e}"

    # calling to our stored procedures:


def get_airline_by_username(username):
    try:
        with engine.connect() as connection:
            # Call the stored procedure with input parameters
            query = text("CALL get_airline_by_username(:username, :airline_id, :airline_name, :country_id, :user_id)")

            # Parameters to pass into the procedure
            params = {
                "username": username,
                "airline_id": None,  # Placeholder for output
                "airline_name": None,  # Placeholder for output
                "country_id": None,  # Placeholder for output
                "user_id": None  # Placeholder for output
            }

            # Execute the query with the parameters as a dictionary
            connection.execute(query, params)

            # The output values will be in the params dictionary
            airline_id = params["airline_id"]
            airline_name = params["airline_name"]
            country_id = params["country_id"]
            user_id = params["user_id"]

            # Return the result as a dictionary
            return {
                "airline_id": airline_id,
                "airline_name": airline_name,
                "country_id": country_id,
                "user_id": user_id
            }

    except Exception as e:
        return f"Error: {e}"



# def get_airline_by_username(username):
#     try:
#         with engine.connect() as connection:
#             # Construct the stored procedure call query
#             query = text("CALL get_airline_by_username(:param0)")
#             # Execute the query and pass the parameters as a dictionary
#             result = connection.execute(query, {"param0": username})
#             # Fetch results if any
#             return result.fetchall() if result.returns_rows else None
#     except Exception as e:
#         print(f"Error: {e}")
#         raise