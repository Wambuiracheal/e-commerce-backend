# from faker import Faker
# from models import Product, Seller

# fake = Faker()

# def seed_products(num_products=20):
#     with app.app_context():  # Add this line to establish the application context
#         # Fetch an existing seller or create one if none exist
#         seller = Seller.query.first()
#         if not seller:
#             seller = Seller(name="Default Seller", email="seller@example.com")
#             db.session.add(seller)
#             db.session.commit()

#         products = []
#         for _ in range(num_products):
#             product = Product(
#                 seller_id=seller.id,  # Assign a valid seller ID
#                 name=fake.word().capitalize(),
#                 description=fake.sentence(),
#                 price=round(fake.random_number(digits=3), 2),
#                 category=fake.word(),
#                 image=f"https://via.placeholder.com/200"  # Replace with actual URLs
#             )
#             products.append(product)

#         db.session.bulk_save_objects(products)
#         db.session.commit()
#         print(f"Seeded {num_products} products successfully!")

# if __name__ == "__main__":
#     seed_products(20)  # Change the number as needed
