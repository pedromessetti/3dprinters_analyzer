from db import Database


def brand_popularity_analysis():
    df = Database.get_data_from_database()
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
    Database.insert_popular_brands(popular_brands_list)


brand_popularity_analysis()