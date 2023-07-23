import mysql.connector
import pandas as pd


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'printers_admin',
            password = 'jqzXQA_ZI$NL2aSx',
            database = '3dprinters_analyzer'
        )
        print("CONNECTION OK")

        self.cur = self.conn.cursor()


    def get_data_from_database(self):
        query = "SELECT * FROM teste"
        df = pd.read_sql_query(query, self.conn)

        self.conn.close()
        print("CONNECTION CLOSED")
        return df


    def insert_popular_brands(self, popular_brands_list):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS popular_brands (
                id INT AUTO_INCREMENT PRIMARY KEY,
                brand VARCHAR(20),
                rating_average DECIMAL(2,1),
                total_reviews INT
            )
        """)

        for item in popular_brands_list:
            self.cur.execute("""
                REPLACE INTO popular_brands (brand, rating_average, total_reviews)
                VALUES (%s, %s, %s)
                           """, (
                item['brand'],
                float(item['rating_average']),
                int(item['total_reviews'])
                ))
            self.conn.commit()

        self.cur.close()
        self.conn.close()
        print("CONNECTION CLOSED")
