# SkyWay Project

## Overview
SkyWay is a robust Python project designed for managing and streamlining operations in an aviation or travel-related domain. It features modular components, a focus on clean architecture, and integration with databases and business logic.

---

## Project Structure
The project is organized into several directories to maintain a clean separation of concerns:

- **`business_logic/`**  
  Contains core business logic, including the `login_token.py` for authentication or session management.

- **`database/`**  
  - `database.py`: Handles database connections and configurations.  
  - `repository.py`: Defines repositories for data access, implementing CRUD operations.

- **`facades/`**  
  - `facades.py`: Provides a higher-level interface to abstract and simplify interaction with the underlying logic and models.

- **`models/`**  
  Represents the data entities and structures used throughout the project:
  - `administrator.py`: Represents administrator users.
  - `airline_company.py`: Manages airline company data.
  - `country.py`: Handles country-related information.
  - `customer.py`: Represents customers in the system.
  - `flight.py`: Defines flight details and schedules.
  - `ticket.py`: Manages ticketing data.
  - `user.py`: Manages general user-related data.
  - `user_role.py`: Handles roles associated with users.

- **`main.py`**  
  The entry point of the application, tying together the various components of the project.

### Docker-Related Files:
- `Dockerfile`: Defines the Docker container for the application.  
- `docker-compose.yml`: Configures services for the development or production environment.

### Configuration and Metadata:
- `.gitignore`: Specifies files and directories to exclude from version control.  
- `requirements.txt`: Lists all Python dependencies required to run the project.

---

## Features
- **User Management:**  
  Support for different user roles such as administrators, airline companies, and customers.

- **Flight Operations:**  
  Management of flights, tickets, and related data.

- **Country Data:**  
  Maintain information about countries for global operations.

- **Authentication:**  
  Includes a login token system for secure authentication and user sessions.

- **Database Integration:**  
  Uses repository patterns for seamless data access and management.

- **Dockerized Deployment:**  
  Ready-to-use Docker configuration for deploying the application in a containerized environment.

---

## Technologies Used
- **Programming Language:** Python 3.x  
- **Frameworks/Libraries:** *(Flask==3.0.0
SQLAlchemy==2.0.36
psycopg2-binary==2.9.9
requests==2.26.0)*  
- **Database:** *SQLite*  
- **Containerization:** Docker, Docker Compose  

---

## Setup Instructions

### Prerequisites
1. Install Python 3.x.  
2. Install Docker and Docker Compose (if using Dockerized deployment).  
3. Install required Python packages:  
   ```bash
   pip install -r requirements.txt
