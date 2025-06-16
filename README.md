# E-commerce Analytics Dashboard

This project consists of a React.js frontend and Flask backend to visualize e-commerce analytics data from PostgreSQL and MongoDB databases.

## Project Structure

```
db-project/
├── frontend/           # React.js frontend
├── backend/           # Flask backend
├── analysis_queries.py # Database analysis scripts
└── docker-compose.yml # Docker configuration
```

## Prerequisites

- Node.js and npm
- Python 3.8+
- Docker and Docker Compose

## Setup Instructions

1. Start the databases:
```bash
docker-compose up -d
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Features

- PostgreSQL Analysis:
  - Top 5 customers by total order value
  - Product category analysis
  - Monthly sales trend

- MongoDB Analysis:
  - Most viewed products
  - User session analysis
  - Hourly traffic analysis

## Technologies Used

- Frontend:
  - React.js
  - Material-UI
  - Recharts
  - TypeScript

- Backend:
  - Flask
  - Flask-CORS
  - psycopg2
  - pymongo

- Databases:
  - PostgreSQL
  - MongoDB 