import pandas as pd
import mysql.connector
import tkinter as tk
from tkinter import ttk
from io import StringIO
from prc import price_range_recommendations
from brand_popularity import brand_popularity_analysis
import sys


def get_data_from_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='printers_admin',
        password='jqzXQA_ZI$NL2aSx',
        database='3dprinters_analyzer'
    )

    query = "SELECT brand, name, price, rating, num_reviews, url FROM printers_table"
    df = pd.read_sql_query(query, connection)

    connection.close()
    return df

def show_price_range_recommendations():
    df = get_data_from_database()
    price_range_recommendations(df)


# Function to display the brand popularity chart in a new window
def show_brand_popularity_chart():
    df = get_data_from_database()
    brand_popularity_analysis(df)

# Create the main Tkinter window
root = tk.Tk()
root.title("3D Printing Market Analysis")
root.geometry("800x600")

# Define a function to close the window
def close_window(event=None):
    root.destroy()

root.bind("<Control-w>", close_window)

# Create buttons to trigger the analysis functions
price_range_button = ttk.Button(root, text="Price Range Recommendations", command=show_price_range_recommendations)
price_range_button.pack(pady=10)

brand_popularity_button = ttk.Button(root, text="Brand Popularity Chart", command=show_brand_popularity_chart)
brand_popularity_button.pack(pady=10)

# Run the main event loop
root.mainloop()