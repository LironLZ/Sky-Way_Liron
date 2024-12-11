from database.database import create_stored_procedures, engine, Base
from flask import Flask
from database.repository import repo_blueprint

app = Flask(__name__)
# Register the blueprint with the main app
app.register_blueprint(repo_blueprint)
def create_db():
    # Create all tables in the database
    print("Creating database schema...")
    Base.metadata.create_all(bind=engine, checkfirst=True)
    create_stored_procedures()
    print("Database schema created successfully!")

# Run the server
if __name__ == '__main__':
    create_db()
    app.run(debug=True)
