from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from collections import defaultdict
import re


class DuplicateCheckPipeline:
    def __init__(self):
        self.seen_items = defaultdict(set)

    def process_item(self, item, spider):
        item_key = (item.get('name'), item.get('brand'), item.get('price'), item.get('rating'),  item.get('num_reviews'))
        if item_key in self.seen_items[spider.name]:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.seen_items[spider.name].add(item_key)
            return item


class PrinterscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Clean name field
        name = adapter.get('name')
        name = name.replace("Official", "").replace("3D Printers", "").replace("3D Printer", "").replace("FDM", "").replace("Resin", "").replace("LCD", "").replace("SLA", "").replace("DLP", "").replace("FFF", "").replace("DIY", "").replace("Kit", "").replace("Printer", "")
        brand = adapter.get('brand')
        if brand.lower() in name.lower():
            name = name.replace(brand, "")
        if ", " in name:
            if name[0] == "," or name[1] == ",":
                name = name[2:]
            else:
                name = name.split(",")[0]

        if "with" in name:
            name = name.split("with")[0]

        if "and" in name:
            name = name.split(" and ")[0]

        if " - " in name:
            name = name.split(" -")[0]

        if "(" in name and ")" in name:
            name = self.remove_parentheses(name)
        
        if "[" in name and "]" in name:
            name = self.remove_squarebracket(name)

        adapter['name'] = name

        
        # Clean brand values
        brand = adapter.get('brand')
        brand = brand.capitalize()
        if " " in brand and brand[1] != " " and brand[2] != " ":
            brand = brand.split(" ")[0]
        adapter['brand'] = brand


        # Remove all whitespaces from all fields except url and date
        to_strip = adapter.field_names()
        for field in to_strip:
            if field != "url" and field != "date":
                value = adapter.get(field)
                value = value.strip()
                adapter[field] = value

        # Remove dots, euro (€) characters and convert to float
        price_keys = ['price']
        for field in price_keys:
            value = adapter.get(field)
            value = value.replace("$", "").replace(",", ".")
            adapter[field] = float(value)

        # Convert rating to float
        rating_keys = ['rating']
        for field in rating_keys:
            value = adapter.get(field)
            value = value.split(" ")[0]
            adapter[field] = float(value)

        # Clean and convert num_reviews to int
        num_reviews_keys = ['num_reviews']
        for field in num_reviews_keys:
            value = adapter.get(field)
            value = value.split(" ")[0]
            adapter[field] = int(value)

        if adapter.get('price') < 90:
            raise DropItem("Price is below 100, dropping item")
        
        # Check if name is empty and remove item if it is
        if not adapter.get('name'):
            raise DropItem(f"Item {item} has an empty name field")

        # Limit name to 30 characters
        name = adapter.get('name')
        adapter['name'] = name[:30]

        return item
                    
    def remove_parentheses(text):
        return re.sub(r'\([^)]*\)', '', text)

    def remove_squarebracket(text):
        return re.sub(r'\[[^)]*\]', '', text)
    

import mysql.connector


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'printers_admin',
            password = 'jqzXQA_ZI$NL2aSx',
            database = '3dprinters_analyzer'
        )

        self.cur = self.conn.cursor()

        # Create table if not exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS amazon_printers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fonte VARCHAR(10),
                date DATE,
                name VARCHAR(30),
                brand VARCHAR(20),
                price DECIMAL(10,2),
                rating DECIMAL(2,1),
                num_reviews INT,
                url VARCHAR(255)
            )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO amazon_printers (fonte, date, name, brand, price, rating, num_reviews, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item.get('fonte'),
            item.get('date'),
            item.get('name'),
            item.get('brand'),
            item.get('price'),
            item.get('rating'),
            item.get('num_reviews'),
            item.get('url')
        ))

        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()