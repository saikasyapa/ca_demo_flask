import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    # Connect to MySQL (without specifying database)
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '1234567890')
    )
    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS ca_demo")
    cursor.execute("USE ca_demo")

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert sample data
    sample_products = [
        ("Cloud Server Basic", "Entry-level cloud server with 2GB RAM and 20GB storage", 29.99),
        ("Cloud Server Pro", "Professional cloud server with 8GB RAM and 100GB storage", 79.99),
        ("Cloud Storage Plus", "Advanced cloud storage solution with 1TB capacity", 49.99),
        ("DevOps Automation Suite", "Complete automation toolkit for CI/CD pipelines", 199.99),
        ("Monitoring Dashboard", "Real-time monitoring and analytics dashboard", 99.99)
    ]

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
            sample_products
        )
        print("Sample data inserted successfully!")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup completed!")

if __name__ == "__main__":
    setup_database()