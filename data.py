urban_routes_url = ' https://cnt-bb85bee5-c2e2-4237-84ba-37ee11d2d8da.containerhub.tripleten-services.com?lng=es'
address_from = 'East 2nd Street, 601'
address_to = '1300 1st St'
phone_number = '+1 123 123 12 12'
card_number, card_code = '1234 5678 9100', '111'
message_for_driver = 'esperando'
payment_type = 'Tarjeta' 
ice_cream_quantity = '2'

headers = {
    "Content-Type": "application/json"
}

user_body = {
    "firstName": "Daniel",
    "phone": "+524988978322",
    "address": "Miami, Florida"
}

kit_body = {
       "name": "Mi conjunto KIT",
       "card": {
           "id": 1,
           "name": "Kit de Prueba"
       },
       "productsList": "null",
       "id": "7",
       "productsCount": "0"
   }