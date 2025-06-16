import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from pymongo import MongoClient
from datetime import datetime, timedelta
import json

# Database connection settings
PG_HOST = "localhost"
PG_PORT = "5433"
PG_DB = "ecommerce_db"
PG_USER = "postgres"
PG_PASSWORD = "postgres"

MONGO_URI = "mongodb://admin:admin@localhost:27018/admin?authSource=admin"
MONGO_DB = "ecommerce_analytics"

def run_postgres_analysis():
    """Run various analytical queries on PostgreSQL data"""
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()

    # 1. Top 5 customers by total order value
    cur.execute("""
        SELECT 
            c.customer_id,
            c.name,
            SUM(od.quantity * p.price) as total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_details od ON o.order_id = od.order_id
        JOIN products p ON od.product_id = p.product_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_spent DESC
        LIMIT 5;
    """)
    top_customers = [{'customer_id': row[0], 'name': row[1], 'total_value': float(row[2])} for row in cur.fetchall()]

    # 2. Product category analysis
    cur.execute("""
        SELECT 
            p.category,
            COUNT(DISTINCT od.order_id) as order_count,
            SUM(od.quantity) as total_quantity,
            AVG(p.price) as avg_price
        FROM products p
        JOIN order_details od ON p.product_id = od.product_id
        GROUP BY p.category
        ORDER BY total_quantity DESC;
    """)
    category_analysis = [{
        'category': row[0],
        'order_count': row[1],
        'total_quantity': row[2],
        'avg_price': float(row[3])
    } for row in cur.fetchall()]

    # 3. Monthly sales trend
    cur.execute("""
        SELECT 
            DATE_TRUNC('month', o.order_date) as month,
            COUNT(DISTINCT o.order_id) as order_count,
            SUM(od.quantity * p.price) as total_revenue
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN products p ON od.product_id = p.product_id
        GROUP BY month
        ORDER BY month;
    """)
    monthly_trend = [{
        'month': row[0].strftime('%Y-%m'),
        'order_count': row[1],
        'total_revenue': float(row[2])
    } for row in cur.fetchall()]

    cur.close()
    conn.close()

    return {
        'topCustomers': top_customers,
        'categoryAnalysis': category_analysis,
        'monthlyTrend': monthly_trend
    }

def run_mongodb_analysis():
    """Run various analytical queries on MongoDB data"""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    web_traffic = db.web_traffic

    # 1. Most viewed products
    pipeline = [
        {"$match": {"event_type": "page_view"}},
        {"$group": {
            "_id": "$product_id",
            "view_count": {"$sum": 1}
        }},
        {"$sort": {"view_count": -1}},
        {"$limit": 5}
    ]
    most_viewed = [{'product_id': result['_id'], 'views': result['view_count']} 
                   for result in web_traffic.aggregate(pipeline)]

    # 2. User session analysis
    pipeline = [
        {"$group": {
            "_id": "$session_id",
            "events": {"$push": "$event_type"},
            "pages": {"$addToSet": "$page"}
        }},
        {"$project": {
            "event_count": {"$size": "$events"},
            "unique_pages": {"$size": "$pages"},
            "has_purchase": {"$in": ["purchase", "$events"]}
        }},
        {"$group": {
            "_id": None,
            "avg_events": {"$avg": "$event_count"},
            "avg_pages": {"$avg": "$unique_pages"},
            "purchase_rate": {
                "$avg": {"$cond": ["$has_purchase", 1, 0]}
            }
        }}
    ]
    session_stats = list(web_traffic.aggregate(pipeline))
    user_session = {
        'avgEventsPerSession': float(session_stats[0]['avg_events']),
        'avgUniquePagesPerSession': float(session_stats[0]['avg_pages']),
        'purchaseConversionRate': float(session_stats[0]['purchase_rate'] * 100)
    }

    # 3. Hourly traffic analysis
    pipeline = [
        {"$project": {
            "hour": {"$hour": {"$toDate": "$timestamp"}},
            "event_type": 1
        }},
        {"$group": {
            "_id": {
                "hour": "$hour",
                "event_type": "$event_type"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.hour": 1, "_id.event_type": 1}}
    ]
    hourly_results = list(web_traffic.aggregate(pipeline))
    
    # Process hourly results into a more usable format
    hourly_traffic = []
    current_hour = None
    hour_data = {}
    
    for result in hourly_results:
        hour = result["_id"]["hour"]
        event_type = result["_id"]["event_type"]
        count = result["count"]
        
        if hour != current_hour:
            if current_hour is not None:
                hourly_traffic.append(hour_data)
            current_hour = hour
            hour_data = {
                'hour': f"{hour:02d}:00",
                'page_view': 0,
                'add_to_cart': 0,
                'cart_view': 0,
                'checkout': 0,
                'purchase': 0,
                'remove_from_cart': 0
            }
        
        hour_data[event_type] = count
    
    if hour_data:
        hourly_traffic.append(hour_data)

    client.close()

    return {
        'mostViewedProducts': most_viewed,
        'userSessionAnalysis': user_session,
        'hourlyTraffic': hourly_traffic
    }

def main():
    try:
        postgres_data = run_postgres_analysis()
        mongodb_data = run_mongodb_analysis()
        
        # Combine the data and output as JSON
        analysis_data = {
            'postgres': postgres_data,
            'mongodb': mongodb_data
        }
        
        # Print the JSON data to stdout
        print(json.dumps(analysis_data))
        
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        raise

if __name__ == "__main__":
    main() 