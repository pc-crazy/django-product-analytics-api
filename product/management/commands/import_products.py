import csv
import os
from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand
from product.models import Product, Category


class Command(BaseCommand):
    help = 'Import products from a CSV file into the Product model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                required_columns = ['name', 'category', 'price', 'stock']
                for col in required_columns:
                    if col not in reader.fieldnames:
                        self.stderr.write(self.style.ERROR(f"Missing required column: {col}"))
                        return

                batch_size = 1000
                products_to_create = []
                total_created = 0

                for row_idx, row in enumerate(reader, start=2):
                    name = row.get('name')
                    category_name = row.get('category')
                    price = row.get('price')
                    stock = row.get('stock')

                    if not name:
                        self.stderr.write(f"Row {row_idx}: Missing product name. Skipping.")
                        continue

                    try:
                        price = Decimal(price)
                        if price < 0:
                            raise ValueError("Negative price")
                    except (InvalidOperation, ValueError, TypeError):
                        self.stderr.write(f"Row {row_idx}: Invalid price '{price}'. Skipping.")
                        continue

                    try:
                        stock_val = int(stock)
                        if stock_val < 0:
                            raise ValueError("Negative stock")
                    except (ValueError, TypeError):
                        self.stderr.write(f"Row {row_idx}: Invalid stock '{stock}'. Skipping.")
                        continue

                    category = None
                    if category_name:
                        category, _ = Category.objects.get_or_create(name=category_name.strip())

                    product = Product(
                        name=name.strip(),
                        category=category,
                        price=price,
                        stock=stock_val,
                    )
                    products_to_create.append(product)

                    if len(products_to_create) >= batch_size:
                        Product.objects.bulk_create(products_to_create, ignore_conflicts=True)
                        total_created += len(products_to_create)
                        self.stdout.write(f"Inserted {total_created} products so far...")
                        products_to_create = []

                if products_to_create:
                    Product.objects.bulk_create(products_to_create, ignore_conflicts=True)
                    total_created += len(products_to_create)

                self.stdout.write(self.style.SUCCESS(f"Import completed. Total products inserted: {total_created}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to process CSV: {e}"))
