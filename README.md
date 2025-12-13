# CourierAPI
CourierAPI is a FastAPI-based application designed for registering, retrieving, and monitoring packages. The API supports advanced filtering and pagination features, enabling seamless management of packages.

## Features

- Register new packages created by couriers with detailed information.
- Retrieve paginated lists of packages with filters for origin state, destination state, classification, and more.
- Retrieve details of a specific package by its ID.
- Integrate RabbitMQ for message queuing to enable downstream processing.
- Extensible and modular design for future enhancements.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Tech Stack

- **Programming Language:** [Python](https://www.python.org/)
- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** PostgreSQL, Redis, SQLite (via SQLAlchemy)
- **Message Queue:** RabbitMQ
- **Testing Frameworks:** Pytest, Unittest
- **Other Tools:** Websockets, Pika, Alembic (for migrations)

---

## Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL
- RabbitMQ

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/ifecog/CourierAPI.git
   cd package-api-python
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Create a `.env` file in the project root:

   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   RABBITMQ_URL=amqp://user:password@localhost:5672/
   RABBITMQ_QUEUE=packages_queue
   ```

5. **Run Migrations**:

   ```bash
   alembic upgrade head
   ```

6. **Start the Application**:

   ```bash
   uvicorn app.main:app --reload
   ```

---

## Usage

### API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### **Packages**

- **Create a Package**: `POST /packages/create`

  - Request Body: `PackageCreate`
  - Response: Created package details

- **Get Packages**: `GET /packages`

  - Query Params: `origin_state`, `destination_state`, `classification`, `tracking_number`, `status`, `start_date`, `end_date`, `page`, `page_size`
  - Response: Paginated list of packages

- **Get a Package by ID**: `GET /packages/{package_id}`
  - Response: Package details

### Example Requests

#### Create a Package

```bash
curl -X POST "http://127.0.0.1:8000/packages/create" -H "Content-Type: application/json" -d '{
  "origin_state": "Lagos",
  "destination_state": "Abuja",
  "classification": "Fragile",
  "status": "Pending",
  "transaction_id": "12345"
}'
```

#### Get Packages

```bash
curl -X GET "http://127.0.0.1:8000/packages?page=1&page_size=10"
```

---

## Testing

### Run Unit Tests

```bash
pytest
```

### Run Integration Tests

```bash
pytest --integration
```

---

## Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
