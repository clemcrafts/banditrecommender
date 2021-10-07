BETA_SHAPE_PARAMETER_A = 2.0
BETA_SHAPE_PARAMETER_B = 2.0

REWARD_ADD_TO_CART = 1.0

CATEGORIES = ["bags", "necklaces", "t-shirts", "jumpers", "cardigans", "skirts"]

KAFKA_CONSUMER_SIZE = 2
KAFKA_CONSUMER_TIMEOUT = 1

TEST_MESSAGES = [{
                "data": {
                    "product_action": {
                        "action": "add_to_cart",
                        "products": [{
                            "id": "P10000",
                            "name": "Black skirt",
                            "brand": "N/A",
                            "category": "skirts",
                            "price": 16.0,
                            "quantity": 1.0,
                            "total_product_amount": 16.0
                        }]
                    },
                },
                "session_id": "11223344",
            }]
