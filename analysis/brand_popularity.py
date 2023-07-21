import pandas as pd
import mysql.connector


def get_data_from_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='printers_admin',
        password='jqzXQA_ZI$NL2aSx',
        database='3dprinters_analyzer'
    )

    query = "SELECT brand, rating, num_reviews FROM amazon_printers"
    df = pd.read_sql_query(query, connection)

    connection.close()
    return df


def brand_popularity_analysis(df):

    brand_rating_average_list = []
    for brand in df['brand'].unique():
        num_reviews = df[df['brand'] == brand]['num_reviews'][df[df['brand'] == brand]['num_reviews'] > 0]
        brand_reviews_sum = num_reviews.sum()
        if brand_reviews_sum > 200:
            ratings = df[df['brand'] == brand]['rating'][df[df['brand'] == brand]['rating'] > 0]
            brand_rating_average = ratings.sum() / ratings.count()
            brand_rating_average_list.append({'brand': brand, 'rating_average': round(brand_rating_average, 2), 'total_reviews': brand_reviews_sum})

    popular_brands_list = sorted(brand_rating_average_list, key=lambda x: x['rating_average'], reverse=True)

    print(popular_brands_list)
    return popular_brands_list


def insert_into_table(popular_brands_list):
    connection = mysql.connector.connect(
        host='localhost',
        user='printers_admin',
        password='jqzXQA_ZI$NL2aSx',
        database='3dprinters_analyzer'
    )

    cursor = connection.cursor()

    for item in popular_brands_list:
        cursor.execute("""
            REPLACE INTO brand_popularity (brand, rating_average, total_reviews)
            VALUES (%s, %s, %s)
                       """, (
            item['brand'],
            float(item['rating_average']),
            int(item['total_reviews'])
            ))
        connection.commit()

    cursor.close()
    connection.close()

df = get_data_from_database()
popular_brands_list = brand_popularity_analysis(df)
insert_into_table(popular_brands_list)