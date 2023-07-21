# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from collections import defaultdict
import re


class DuplicateCheckPipeline:
    def __init__(self):
        self.seen_items = defaultdict(set)

    def process_item(self, item, spider):
        item_key = (item.get('name'), item.get('brand'), item.get('price'), item.get('stars'),  item.get('num_reviews'))
        if item_key in self.seen_items[spider.name]:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.seen_items[spider.name].add(item_key)
            return item


class PrinterscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Clean field values
        name_keys = ['name']
        for field in name_keys:
            value = adapter.get(field)
            value = value.replace("Official ", "").replace("3D ", "").replace("Printer ", "").replace("Printers", "")
            if ", " in value:
                if value[0] == ",":
                    value = value[2:]
                else:
                    value = value.split(",")[0]

            if "with" in value:
                value = value.split("with")[0]

            if " and " in value:
                value = value.split(" and ")[0]

            if " -" in value:
                value = value.split(" -")[0]

            if "(" in value and ")" in value:
                value = self.remove_parentheses(value)
            
            value = value.replace(",", "")

            adapter[field] = value

        
        # Clean field values
        brand_keys = ['brand']
        for field in brand_keys:
            value = adapter.get(field)
            if value[0].islower():
                value = value.capitalize()
            if " " in value and value[1] != " " and value[2] != " ":
                value = value.split(" ")[0]
            adapter[field] = value

        name = adapter.get('name')
        brand = adapter.get('brand')
        if brand.lower() in name.lower():
            name = name.replace(brand, "")
            adapter['name'] = name

        # Remove all whitespaces
        to_strip = adapter.field_names()
        for field in to_strip:
            if field is not "url" and field is not "date":
                value = adapter.get(field)
                adapter[field] = value.strip()

        # Remove dots, euro (€) characters and convert to float
        price_keys = ['price']
        for field in price_keys:
            value = adapter.get(field)
            value = value.replace("$", "").replace(",", ".")
            adapter[field] = float(value)

        # Convert stars to float
        stars_keys = ['stars']
        for field in stars_keys:
            value = adapter.get(field)
            value = value.split(" ")[0]
            adapter[field] = float(value)

        # Convert num_reviews to int
        num_reviews_keys = ['num_reviews']
        for field in num_reviews_keys:
            value = adapter.get(field)
            value = value.split(" ")[0]
            adapter[field] = int(value)

        if adapter.get('price') < 100:
            raise DropItem("Price is below 100, dropping item")
        
        # Check if name is empty and remove item if it is
        if not adapter.get('name'):
            raise DropItem(f"Item {item} has an empty name field")

        # Limit name to 30 characters
        name = adapter.get('name')
        adapter['name'] = name[:30]

        # Remove spaces and measure units from area
        #area_keys = ['area']
        #for field in area_keys:
        #    value = adapter.get(field)
        #    if "x" not in value:
        #        adapter[field] = "Not specified"
        #    else:
        #        adapter[field] = value.replace("mm", "").replace(" ", "").replace("Ø", "")

        return item
                    
    def remove_parentheses(text):
        return re.sub(r'\([^)]*\)', '', text)            




import mysql.connector


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'printers_admin',
            password = 'jqzXQA_ZI$NL2aSx',
            database = 'printers'
        )

        self.cur = self.conn.cursor()

        # Create table if not exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS test (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fonte VARCHAR(10),
                date DATE,
                name VARCHAR(30),
                brand VARCHAR(20),
                price DECIMAL(10,2),
                stars DECIMAL(2,1),
                num_reviews INT,
                url VARCHAR(255)
            )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO test (fonte, date, name, brand, price, stars, num_reviews, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item.get('fonte'),
            item.get('date'),
            item.get('name'),
            item.get('brand'),
            item.get('price'),
            item.get('stars'),
            item.get('num_reviews'),
            item.get('url')
        ))

        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()