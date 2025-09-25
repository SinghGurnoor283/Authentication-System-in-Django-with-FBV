from account.models import Product

# PERMISSION_CONFIG={
#     'customer':[
#         "view_profile",
#         "update_profile",
#         "change_password",
#     ],
#     "seller": [
#         "view_profile",
#         "update_profile",
#         "change_password",
#         "manage_customers",  # only seller can do this
#     ],
# }


from account.models import Product

PERMISSION_CONFIG = {
    "customer": {
        Product: ["view"]   # will map to "view_product"
    },
    "seller": {
        Product: ["add", "change", "delete", "view"]  # full access
    }
}
