from django.core.management.base import BaseCommand

from catalog.models import Category, Product, Tag


class Command(BaseCommand):
    help = "Wipe the entries and repopulate the catalog with example categories, tags, and products"
    #function to handle the command that first wipes the previous data, and then creates new categories, tags, and products with relationships
    def handle(self, *args, **options):
        #wipe existing data to avoid duplicates and collision
        Product.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()

        #create categories and tags
        cats = {
            name: Category.objects.create(name=name)
            for name in ["furniture", "food", "sport", "clothing", "car"]
        }

        tags = {
            name: Tag.objects.create(name=name)
            for name in [
                "bestseller", "new arrival", "on sale", "premium", "eco-friendly",
                "lightweight", "durable", "imported", "handmade", "limited edition",
            ]
        }

        #create data for products with relationships to newly created categories and tags
        data = [
            ("Dining table",   "Large wooden dining table for six people",       "furniture", ["premium", "durable"],           450),
            ("Office chair",   "Ergonomic mesh office chair with back support",  "furniture", ["bestseller", "durable"],        190),
            ("Bookshelf",      "Tall wooden bookshelf with five shelves",        "furniture", ["durable", "handmade"],          120),
            ("Floor lamp",     "Modern standing floor lamp with warm light",     "furniture", ["new arrival", "premium"],        80),
            ("Green apple",    "Fresh crisp green apple, locally grown",         "food",      ["eco-friendly", "on sale"],         1),
            ("Chocolate bar",  "Dark chocolate bar with roasted almonds",        "food",      ["bestseller", "imported"],          3),
            ("Coffee beans",   "Premium arabica coffee beans, dark roast",       "food",      ["premium", "imported"],            15),
            ("Olive oil",      "Extra virgin olive oil, cold pressed",           "food",      ["premium", "eco-friendly"],        12),
            ("Tennis racket",  "Lightweight carbon tennis racket for beginners", "sport",     ["lightweight", "bestseller"],      95),
            ("Yoga mat",       "Non-slip yoga mat, extra thick and comfortable", "sport",     ["eco-friendly", "on sale"],        25),
            ("Dumbbell set",   "Adjustable dumbbell set for home workouts",      "sport",     ["durable", "bestseller"],         140),
            ("Bicycle helmet", "Lightweight bicycle helmet with air vents",      "sport",     ["lightweight", "new arrival"],     60),
            ("Denim jacket",   "Classic blue denim jacket with a regular fit",   "clothing",  ["bestseller", "durable"],          70),
            ("Wool scarf",     "Warm wool scarf for cold winter days",           "clothing",  ["handmade", "imported"],           30),
            ("Running shoes",  "Breathable running shoes with cushioned soles",  "clothing",  ["lightweight", "new arrival"],     85),
            ("Leather belt",   "Genuine leather belt, handcrafted",              "clothing",  ["handmade", "premium"],            40),
            ("Brake pads",     "Ceramic brake pads for improved stopping power", "car",       ["durable", "imported"],            55),
            ("Car battery",    "Long-life 12V car battery, maintenance free",    "car",       ["durable", "premium"],            130),
            ("Dash camera",    "Full HD dash camera with night vision",          "car",       ["new arrival", "bestseller"],      90),
            ("Roof rack",      "Aluminum roof rack, lightweight and sturdy",     "car",       ["lightweight", "limited edition"], 160),
        ]

        #create entries for products in DB
        for name, description, category, tag_names, price in data:
            product = Product.objects.create(
                name=name,
                description=description,
                category=cats[category],
                price=price,
            )
            product.tags.set([tags[t] for t in tag_names])

        #print result message
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {Category.objects.count()} categories, "
                f"{Tag.objects.count()} tags, {Product.objects.count()} products."
            )
        )
