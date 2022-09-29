from telebot.types import ShippingOption, LabeledPrice
from .shipping_product import Product


def generate_product_invoice(product_data):
    query = Product(
        title="Shop Bot",
        description='\n'.join([title for title in product_data]),
        currency='UZS',
        prices = [LabeledPrice(
            label=f"{product_data[title]['quantity']} {title}",
            amount=int(product_data[title]['quantity']) * int(product_data[title]['price']) * 100)
        for title in product_data
        ],
        start_parameter='create_invoice_products',
        need_name=True,
        need_phone_number=True,
        is_flexible=True
    )
    return query

EXPRESS_SHIPPING = ShippingOption(
    id='post_express',
    title='for 3 hour').add_price(LabeledPrice('for 3 hour', 2500000)
)

REGULAR_SHIPPING = ShippingOption(
    id='post_pickup',
    title='Pickup').add_price(LabeledPrice('Pickup', 0)
)
REGIONS_SHIPPING = ShippingOption(
    id='post_region',
    title="All regions in Uzbekistan").add_price(LabeledPrice("All regions in Uzbekistan", 20000000)
)

