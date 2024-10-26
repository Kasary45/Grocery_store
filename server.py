from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from sql_connection import get_sql_connection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

####product_page
#1) function of get all products
def get_all_products():
    cnx = get_sql_connection()
    cursor = cnx.cursor()
    query = """
        SELECT p.product_id, p.name, u.uom_name, p.price_per_unit 
        FROM products p  
        INNER JOIN uom u ON p.uom_id = u.uom_id
    """
    cursor.execute(query)
    response = []

    for (product_id, name, uom_name, price_per_unit) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_name': uom_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()
    return response

#2) insert new product
def insert_new_product(product_data):
    # Insert a new product into the database
    cnx = get_sql_connection()
    cursor = cnx.cursor()
    try:
        insert_query = """
        INSERT INTO products (name, uom_id, price_per_unit) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (product_data['product_name'], product_data['uom_id'], product_data['price_per_unit']))
        cnx.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted product
    except Exception as e:
        print("Error inserting product:", e)
        return None
    finally:
        cursor.close()

#3) Delete selected product
def delete_product(product_id):  # Accept product_id as a parameter
    cnx = get_sql_connection()
    cursor = cnx.cursor()
    try:
        delete_query = "DELETE FROM products WHERE product_id = %s"
        cursor.execute(delete_query, (product_id,))
        cnx.commit()
        return product_id  # Return the ID of the deleted product
    except Exception as e:
        print("Error deleting product:", e)
        return None
    finally:
        cursor.close()



#4) get unit of measurement as pop up
def get_uoms():
    cnx = get_sql_connection()  # Establishing the connection to the database
    cursor = cnx.cursor()  # Creating a cursor object for database operations
    query = "SELECT uom_id, uom_name FROM uom"  # SQL query to fetch UOM data
    cursor.execute(query)  # Executing the query

    response = []  # Initializing an empty list to hold the response data
    for (uom_id, uom_name) in cursor:  # Looping through each row in the query result
        response.append({
            'uom_id': uom_id,  # Appending UOM ID
            'uom_name': uom_name  # Appending UOM name
        })

    cursor.close()  # Closing the cursor
     # Closing the connection

    return response  # Returning the response as a list of UOM dictionaries

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Endof product function  page@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
########################################################################################################################
##flask routs for product_page

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = get_all_products()
    return jsonify(products)


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = request.json  # Get JSON data directly

    # Check if the required fields are present and valid
    if 'product_name' not in request_payload or 'uom_id' not in request_payload or 'price_per_unit' not in request_payload:
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

    # Check if uom_id is valid
    if request_payload['uom_id'] is None or not isinstance(request_payload['uom_id'], int):
        return jsonify({'status': 'error', 'message': 'Invalid UOM ID'}), 400

    product_id = insert_new_product(request_payload)

    if product_id is not None:
        return jsonify({'status': 'success', 'product_id': product_id}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Failed to insert product'}), 500



#
# # CORS setup if needed
# @app.after_request
# def after_request(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
#     response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
#     return response




@app.route('/deleteproduct', methods=['POST'])
def delete_product_route():
    try:
        # Getting the product ID from the JSON payload
        request_data = request.get_json()
        product_id = request_data.get('product_id')

        if product_id is None:
            return jsonify({'status': 'error', 'message': 'Product ID is required'}), 400

        return_id = delete_product(product_id)  # Call the standalone function

        if return_id:  # Assuming it returns the deleted ID or None
            return jsonify({'status': 'success', 'product_id': return_id}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
    except Exception as e:
        print("Error while deleting product:", str(e))
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500








@app.route('/getUOM', methods=['GET'])
def get_uom_endpoint():
    try:
        uoms = get_uoms()  # Fetch UOM data
        response = jsonify(uoms)  # Convert to JSON
        response.headers.add('Access-Control-Allow-Origin', '*')  # Allow CORS
        return response
    except Exception as e:
        print("Error fetching UOMs:", e)  # Log error for debugging
        return jsonify({'error': 'Failed to fetch UOMs'}), 500  # Error handlin



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Endof product function  flask-page@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
########################################################################################################################

def insert_order(order_payload):
    cnx = get_sql_connection()
    cursor = cnx.cursor()

    # Insert order
    order_query = (
        "INSERT INTO orders (customer_name, total_cost, datetime) "
        "VALUES (%s, %s, %s)"
    )
    order_data = (order_payload['customer_name'], order_payload['total_cost'], datetime.now())
    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    # Insert order details
    order_details_query = (
        "INSERT INTO order_details (order_id, product_id, quantity, total_price) "
        "VALUES (%s, %s, %s, %s)"
    )
    order_details_data = [
        (order_id, detail['product_id'], detail['quantity'], detail['total_price'])
        for detail in order_payload['order_details']
    ]

    cursor.executemany(order_details_query, order_details_data)
    cnx.commit()

    # Close the cursor and connection
    cursor.close()


    return order_id

def get_all_orders():
    cnx=get_sql_connection()
    cursor=cnx.cursor()
    query="SELECT * FROM orders"
    cursor.execute(query)
    response=[]
    for (order_id,customer_name,total_cost,dt) in cursor:
        response.append({
            'order_id':order_id,
            'customer_name':customer_name,
            'total_cost':total_cost,
            'datetime':dt

        })

    return response


@app.route('/getAllOrders', methods=['GET'])
def get_orders():
    products = get_all_orders()
    response = jsonify(products)

    # Correcting the header name
    response.headers.add('Access-Control-Allow-Origin', '*')

    # Return the response directly
    return response


# @app.route('/insertOrder', methods=['POST'])
# def insert_order_route():
#     request_payload = request.json  # Get JSON data directly
#
#     # Check if required fields are present
#     if 'customer_name' not in request_payload or 'total_cost' not in request_payload or 'order_details' not in request_payload:
#         return jsonify({'status': 'error', 'message': 'All fields are required'}), 400
#
#     # Check if total_cost is a valid number
#     try:
#         total_cost = float(request_payload['total_cost'])
#         if total_cost <= 0:
#             return jsonify({'status': 'error', 'message': 'Total cost must be greater than zero'}), 400
#     except ValueError:
#         return jsonify({'status': 'error', 'message': 'Total cost must be a valid number'}), 400
#
#     # Check if order_details is a list and not empty
#     if not isinstance(request_payload['order_details'], list) or len(request_payload['order_details']) == 0:
#         return jsonify({'status': 'error', 'message': 'Order details must be provided'}), 400
#
#     # Loop through each order detail to validate
#     for detail in request_payload['order_details']:
#         if 'product_id' not in detail or 'quantity' not in detail or 'total_price' not in detail:
#             return jsonify({'status': 'error', 'message': 'All fields in order details are required'}), 400
#
#         if detail['quantity'] <= 0 or detail['total_price'] <= 0:
#             return jsonify({'status': 'error', 'message': 'Quantity and total price must be greater than zero'}), 400
#
#     # Now you can insert the order into your database
#     order_id = insert_order(request_payload)
#
#     if order_id is not None:
#         return jsonify({'status': 'success', 'order_id': order_id}), 201
#     else:
#         return jsonify({'status': 'error', 'message': 'Failed to insert order'}), 500








@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = request.json  # Get JSON data directly

    # Check if required fields are present
    if 'customer_name' not in request_payload or 'total_cost' not in request_payload or 'order_details' not in request_payload:
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

    # Check if order_details is a list and not empty
    if not isinstance(request_payload['order_details'], list) or len(request_payload['order_details']) == 0:
        return jsonify({'status': 'error', 'message': 'Order details must be provided'}), 400

    # Loop through each order detail to validate
    for detail in request_payload['order_details']:
        if 'product_id' not in detail or 'quantity' not in detail or 'total_price' not in detail:
            return jsonify({'status': 'error', 'message': 'All fields in order details are required'}), 400

        if detail['quantity'] <= 0 or detail['total_price'] <= 0:
            return jsonify({'status': 'error', 'message': 'Quantity and total price must be greater than zero'}), 400

    # Now you can insert the order into your database
    order_id = insert_order(request_payload)  # Use a different function for DB insertion

    if order_id is not None:
        return jsonify({'status': 'success', 'order_id': order_id}), 201
    else:
        return jsonify({'status': 'error', 'message': 'Failed to insert order'}), 500




if __name__=='__main__':
    app.run(debug=True)