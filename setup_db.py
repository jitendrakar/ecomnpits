import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='root', port=3306)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ecom_npits CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cursor.execute("CREATE USER IF NOT EXISTS 'ecom_npits'@'localhost' IDENTIFIED BY 'ecom_npits_pass123';")
    cursor.execute("GRANT ALL PRIVILEGES ON ecom_npits.* TO 'ecom_npits'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")
    print("MySQL database 'ecom_npits' and user 'ecom_npits' created successfully!")
    conn.close()
except Exception as e:
    print(f"Error setting up database: {e}")
