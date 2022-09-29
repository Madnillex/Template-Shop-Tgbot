from loader import bot

# db.create_table_users()
# db.create_table_categories()
# db.create_table_products()
#
# db.insert_category_name('TV')
# db.insert_category_name('Tables')
# db.insert_category_name('Phones')
# db.insert_category_name('Air conditioners')
#
# products = [OpenShopParser('phones').get_info(),
#             OpenShopParser('-C7V2C').get_info(),
#             OpenShopParser('air-conditioners').get_info(),
#             OpenShopParser('tv').get_info()]
#
# for category in products:
#     for product in category:
#         product_name = product['title']
#         link = product['link']
#         price = product['price']
#         image = product['image']
#         category_id = product['category_id']
#
#         db.insert_product_to_products(product_name, price, image, link, category_id)


if __name__ == '__main__':
    bot.infinity_polling()

