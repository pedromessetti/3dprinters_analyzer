from db import Database


def top_rated_printers():
    db = Database()
    df = db.get_data()
    top_rated_list = []
    for name in df['name'].unique():
        num_reviews = df[df['name'] == name]['num_reviews'][df[df['name'] == name]['num_reviews'] > 0]
        name_reviews_sum = num_reviews.sum()
        if name_reviews_sum > 200:
            ratings = df[df['name'] == name]['rating'][df[df['name'] == name]['rating'] > 0]
            top_rated_list.append({'name': name, 'rating': ratings, 'total_reviews': name_reviews_sum})
    print(top_rated_list)

top_rated_printers()
