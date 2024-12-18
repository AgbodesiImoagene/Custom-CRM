# Gong Custom CRM

## Overview

This project is a custom CRM (Customer Relationship Management) system built using FastAPI, SQLAlchemy, and Alembic. It provides endpoints for managing users, contacts, deals, companies, and leads.

## Getting Started

### Prerequisites

- Python 3.8+
- SQLite (or another database supported by SQLAlchemy)
- Virtual environment tool (e.g., `venv` or `virtualenv`)
- Node.js and npm (for initial setup, not required for hosting)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/gong_custom_CRM.git
   cd gong_custom_CRM
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the environment variables:**

   Create a `.env` file in the root directory and add the following:

   ```env
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY=your_secret_key
   ```

5. **Run the database migrations:**

   ```sh
   alembic upgrade head
   ```

### Running the Application

1. **Start the FastAPI server:**

   ```sh
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation:**

   Open your browser and navigate to `http://127.0.0.1:8000/docs` to see the interactive API documentation provided by Swagger UI.

### Running Tests

1. **Run the tests using pytest:**

   ```sh
   pytest
   ```

### Setting Up the Frontend

1. **Navigate to the frontend directory:**

   ```sh
   cd frontend
   ```

2. **Update the `env.js` file**

    Open the Open the `env.js` file and update the `BASE_URL` to point to the URL of your backend setup. For example:

    ```javascript
    const BASE_URL = 'http://127.0.0.1:8000';
    ```

3. **Serve the frontend using a static file server:**

    You can use any static file server to serve the contents of the `frontend` directory. For example, using `serve`:

    ```sh
    npm install -g serve
    serve .
    ```

### Hosting the frontend

1. **Build the frontend:**

    ```sh
    npm run build
    ```

    This will create a `dist` directory with the production build of the frontend.

2. **Serve the frontend using a static file server:**

    You can use any static file server to serve the contents of the `dist` directory. For example, using `serve`:

    ```sh
    npm install -g serve
    serve -s dist
    ```

## API Endpoints

The API provides the following endpoints:

- **Auth:**

  - `POST /auth/token`: Login and get an access token
  - `POST /auth/generate-api-key`: Generate an API key for the current user
  - `POST /auth/basic-auth`: Login with basic authentication

- **Users:**

  - `POST /users/`: Create a new user
  - `GET /users/`: Get a list of users
  - `GET /users/{user_id}`: Get a user by ID
  - `PUT /users/{user_id}`: Update a user by ID

- **Contacts:**

  - `POST /contacts/`: Create a new contact
  - `GET /contacts/`: Get a list of contacts
  - `GET /contacts/{contact_id}`: Get a contact by ID
  - `PUT /contacts/{contact_id}`: Update a contact by ID
  - `DELETE /contacts/{contact_id}`: Delete a contact by ID

- **Deals:**

  - `POST /deals/`: Create a new deal
  - `GET /deals/`: Get a list of deals
  - `GET /deals/{deal_id}`: Get a deal by ID
  - `PUT /deals/{deal_id}`: Update a deal by ID
  - `DELETE /deals/{deal_id}`: Delete a deal by ID

- **Companies:**

  - `POST /companies/`: Create a new company
  - `GET /companies/`: Get a list of companies
  - `GET /companies/{company_id}`: Get a company by ID

- **Leads:**
  - `POST /leads/`: Create a new lead
  - `GET /leads/`: Get a list of leads
  - `GET /leads/{lead_id}`: Get a lead by ID
  - `PUT /leads/{lead_id}`: Update a lead by ID
  - `DELETE /leads/{lead_id}`: Delete a lead by ID
