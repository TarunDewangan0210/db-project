// Create root user with all necessary permissions
db = db.getSiblingDB('admin');

db.createUser({
  user: 'admin',
  pwd: 'admin',
  roles: [
    { role: 'userAdminAnyDatabase', db: 'admin' },
    { role: 'readWriteAnyDatabase', db: 'admin' },
    { role: 'dbAdminAnyDatabase', db: 'admin' },
    { role: 'clusterAdmin', db: 'admin' }
  ]
});

// Switch to application database
db = db.getSiblingDB('ecommerce_analytics');

// Create collection to ensure database exists
db.createCollection('web_traffic');

// Create indexes
db.web_traffic.createIndex({ "timestamp": 1 });
db.web_traffic.createIndex({ "product_id": 1 });
db.web_traffic.createIndex({ "user_id": 1 }); 