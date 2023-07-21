import pandas as pd
import tkinter as tk

def price_range_recommendations(df):
    df['price_range'] = pd.cut(df['price'], bins=[0, 200, 400, float('inf')], labels=['Budget', 'Mid-Range', 'Premium'])

    budget_customers = df[(df['rating'] >= 4) & (df['num_reviews'] >= 50) & (df['price_range'] == 'Budget')]
    mid_range_customers = df[(df['rating'] >= 4.5) & (df['num_reviews'] >= 100) & (df['price_range'] == 'Mid-Range')]
    premium_customers = df[(df['rating'] >= 4.8) & (df['num_reviews'] >= 100) & (df['price_range'] == 'Premium')]

    root = tk.Tk()
    root.title("Price Range")
    root.geometry("800x800")

    # Create a label for each customer segment and put the price range recommendations in the label
    budget_label = tk.Label(root, text="Budget Customers: " + str(budget_customers['price'].min()) + " - " + str(budget_customers['price'].max()) + "\nPrinters for Budget Customers:\n" + str(budget_customers[['brand', 'name']]))
    budget_label.pack()

    mid_range_label = tk.Label(root, text="Mid-Range Customers: " + str(mid_range_customers['price'].min()) + " - " + str(mid_range_customers['price'].max()) + "\nPrinters for Mid-Range Customers:\n" + str(mid_range_customers[['brand', 'name']]))
    mid_range_label.pack()

    premium_label = tk.Label(root, text="Premium Customers: " + str(premium_customers['price'].min()) + " - " + str(premium_customers['price'].max()) + "\nPrinters for Premium Customers:\n" + str(premium_customers[['brand', 'name']]))
    premium_label.pack()

    root.mainloop()
