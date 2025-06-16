# E-commerce Analytics Platform Documentation

## Table of Contents
1. [Getting Started](#getting-started)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Data Flow](#data-flow)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Frontend Components](#frontend-components)
8. [Setup and Deployment](#setup-and-deployment)
9. [Performance Considerations](#performance-considerations)

## Getting Started

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone <repository-url>
cd db-project

# Verify the project structure
ls -la
```

Expected directory structure:
```
db-project/
├── frontend/           # React.js frontend
├── backend/           # Flask backend
├── docs/             # Documentation
├── analysis_queries.py # Database analysis scripts
└── docker-compose.yml # Docker configuration
```

### Step 2: Set Up the Databases
```bash
# Start PostgreSQL and MongoDB containers
docker-compose up -d

# Verify containers are running
docker ps

# Expected output should show:
# - ecommerce_postgres (PostgreSQL)
# - ecommerce_mongodb (MongoDB)
# - pgadmin (Optional)
```

### Step 3: Set Up the Backend
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list

# Start the Flask server
python app.py
```

Expected output:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5001
```

### Step 4: Set Up the Frontend
```bash
# Open a new terminal
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

Expected output:
```
Compiled successfully!

You can now view analysis-dashboard in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### Step 5: Verify the Setup
1. **Check Database Connections**
   ```bash
   # Test PostgreSQL connection
   psql -h localhost -p 5433 -U postgres -d ecommerce_db
   # Password: postgres
   
   # Test MongoDB connection
   mongosh "mongodb://admin:admin@localhost:27018/admin?authSource=admin"
   ```

2. **Test API Endpoint**
   ```bash
   # Using curl
   curl http://localhost:5001/api/analysis
   
   # Or using browser
   # Open http://localhost:5001/api/analysis
   ```

3. **Access the Dashboard**
   - Open http://localhost:3000 in your browser
   - You should see the analytics dashboard with charts

### Step 6: Development Workflow
1. **Backend Development**
   ```bash
   # Make sure you're in the backend directory
   cd backend
   
   # Activate virtual environment if not already activated
   source venv/bin/activate
   
   # Run the Flask server with auto-reload
   python app.py
   ```

2. **Frontend Development**
   ```bash
   # Make sure you're in the frontend directory
   cd frontend
   
   # Start the development server
   npm start
   ```

3. **Database Management**
   ```bash
   # Stop all containers
   docker-compose down
   
   # Start containers
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   ```

### Step 7: Troubleshooting
1. **Database Connection Issues**
   ```bash
   # Check if containers are running
   docker ps
   
   # Check container logs
   docker logs ecommerce_postgres
   docker logs ecommerce_mongodb
   
   # Restart containers if needed
   docker-compose restart
   ```

2. **Backend Issues**
   ```bash
   # Check Flask server logs
   # Look for error messages in the terminal where app.py is running
   
   # Verify Python environment
   which python
   pip list
   ```

3. **Frontend Issues**
   ```bash
   # Clear npm cache
   npm cache clean --force
   
   # Remove node_modules and reinstall
   rm -rf node_modules
   npm install
   
   # Check for port conflicts
   lsof -i :3000
   ```

### Step 8: Stopping the Application
```bash
# Stop the frontend (Ctrl+C in the frontend terminal)
# Stop the backend (Ctrl+C in the backend terminal)

# Stop the databases
docker-compose down

# Optional: Remove all containers and volumes
docker-compose down -v
```

## System Architecture

### Overview
The E-commerce Analytics Platform is a full-stack application that combines PostgreSQL and MongoDB databases to provide comprehensive analytics for an e-commerce system. The architecture follows a modern microservices approach with clear separation of concerns.

```mermaid
graph TD
    A[React Frontend] --> B[Flask Backend API]
    B --> C[PostgreSQL Database]
    B --> D[MongoDB Database]
    E[Analysis Scripts] --> C
    E --> D
```

### Components
1. **Frontend Layer**
   - React.js application with TypeScript
   - Material-UI for component styling
   - Recharts for data visualization
   - Axios for API communication

2. **Backend Layer**
   - Flask REST API
   - CORS support for cross-origin requests
   - JSON response formatting
   - Error handling and logging

3. **Database Layer**
   - PostgreSQL for structured data
   - MongoDB for unstructured/analytics data
   - Docker containers for isolation

## Technology Stack

### Frontend
- **Framework**: React.js 18.2.0
- **Language**: TypeScript 4.9.5
- **UI Library**: Material-UI 5.15.10
- **State Management**: React Hooks
- **Data Visualization**: Recharts 2.12.0
- **HTTP Client**: Axios 1.6.7

### Backend
- **Framework**: Flask 3.0.2
- **Language**: Python 3.8+
- **Database Drivers**:
  - psycopg2-binary 2.9.9 (PostgreSQL)
  - pymongo 4.6.1 (MongoDB)
- **CORS Support**: flask-cors 4.0.0
- **Environment Management**: python-dotenv 1.0.1

### Databases
- **PostgreSQL**
  - Version: Latest
  - Port: 5433
  - Purpose: Structured data storage

- **MongoDB**
  - Version: Latest
  - Port: 27018
  - Purpose: Analytics and web traffic data

### Development Tools
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git
- **Package Management**:
  - npm (Frontend)
  - pip (Backend)

## Data Flow

### 1. Data Collection
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant PostgreSQL
    participant MongoDB

    User->>Frontend: Interacts with website
    Frontend->>Backend: Sends analytics data
    Backend->>MongoDB: Stores web traffic
    Backend->>PostgreSQL: Stores transaction data
```

### 2. Data Analysis
```mermaid
sequenceDiagram
    participant Frontend
    participant Backend
    participant Analysis
    participant PostgreSQL
    participant MongoDB

    Frontend->>Backend: Requests analytics
    Backend->>Analysis: Triggers analysis
    Analysis->>PostgreSQL: Queries transaction data
    Analysis->>MongoDB: Queries web traffic
    Analysis->>Backend: Returns processed data
    Backend->>Frontend: Sends formatted results
```

## Database Schema

### PostgreSQL Tables

1. **customers**
   ```sql
   CREATE TABLE customers (
       customer_id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       email VARCHAR(100),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

2. **products**
   ```sql
   CREATE TABLE products (
       product_id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       category VARCHAR(50),
       price DECIMAL(10,2),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. **orders**
   ```sql
   CREATE TABLE orders (
       order_id SERIAL PRIMARY KEY,
       customer_id INTEGER REFERENCES customers(customer_id),
       order_date TIMESTAMP,
       total_amount DECIMAL(10,2),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

4. **order_details**
   ```sql
   CREATE TABLE order_details (
       order_detail_id SERIAL PRIMARY KEY,
       order_id INTEGER REFERENCES orders(order_id),
       product_id INTEGER REFERENCES products(product_id),
       quantity INTEGER,
       unit_price DECIMAL(10,2),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

### MongoDB Collections

1. **web_traffic**
   ```javascript
   {
     session_id: String,
     user_id: String,
     product_id: Number,
     event_type: String,
     timestamp: Date,
     page: String
   }
   ```

## API Endpoints

### GET /api/analysis
Returns comprehensive analytics data from both databases.

**Response Format:**
```json
{
  "postgres": {
    "topCustomers": [
      {
        "customer_id": number,
        "name": string,
        "total_value": number
      }
    ],
    "categoryAnalysis": [
      {
        "category": string,
        "order_count": number,
        "total_quantity": number,
        "avg_price": number
      }
    ],
    "monthlyTrend": [
      {
        "month": string,
        "order_count": number,
        "total_revenue": number
      }
    ]
  },
  "mongodb": {
    "mostViewedProducts": [
      {
        "product_id": number,
        "views": number
      }
    ],
    "userSessionAnalysis": {
      "avgEventsPerSession": number,
      "avgUniquePagesPerSession": number,
      "purchaseConversionRate": number
    },
    "hourlyTraffic": [
      {
        "hour": string,
        "page_view": number,
        "add_to_cart": number,
        "cart_view": number,
        "checkout": number,
        "purchase": number,
        "remove_from_cart": number
      }
    ]
  }
}
```

## Frontend Components

### Dashboard Component
- Displays all analytics data in a grid layout
- Uses Material-UI components for consistent styling
- Implements responsive design for all screen sizes

### Charts
1. **Top Customers Chart**
   - Bar chart showing top 5 customers by total order value
   - Interactive tooltips and legends

2. **Category Analysis Chart**
   - Bar chart showing sales by product category
   - Color-coded bars for different categories

3. **Hourly Traffic Chart**
   - Multi-series bar chart showing different event types
   - Time-based x-axis with event counts

## Setup and Deployment

### Prerequisites
- Node.js and npm
- Python 3.8+
- Docker and Docker Compose
- Git

### Local Development Setup
1. Clone the repository
2. Start the databases:
   ```bash
   docker-compose up -d
   ```

3. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

5. Start the services:
   - Backend: `python app.py`
   - Frontend: `npm start`

### Production Deployment
1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Configure environment variables
3. Set up a production WSGI server
4. Configure reverse proxy (e.g., Nginx)
5. Set up SSL certificates

## Performance Considerations

### Database Optimization
1. **PostgreSQL**
   - Indexes on frequently queried columns
   - Partitioning for large tables
   - Regular VACUUM and ANALYZE

2. **MongoDB**
   - Indexes on query fields
   - Proper sharding strategy
   - Regular maintenance

### Application Performance
1. **Frontend**
   - Code splitting
   - Lazy loading of components
   - Optimized bundle size

2. **Backend**
   - Connection pooling
   - Caching strategies
   - Asynchronous processing

### Monitoring
- Database performance metrics
- API response times
- Error rates and types
- Resource utilization

## Security Considerations

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control
   - Secure session management

2. **Data Protection**
   - Encrypted data transmission
   - Secure password storage
   - Regular security audits

3. **API Security**
   - Rate limiting
   - Input validation
   - CORS configuration

## Future Enhancements

1. **Features**
   - Real-time analytics
   - Custom report generation
   - Advanced filtering options

2. **Technical**
   - Microservices architecture
   - Message queue integration
   - Enhanced caching

3. **Scalability**
   - Horizontal scaling
   - Load balancing
   - Database sharding 