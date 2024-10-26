import mysql.connector
from mysql.connector import Error
import time

__cnx = None  # Global variable to hold the connection

def get_sql_connection():
    global __cnx
    if __cnx is None:
        try:
            __cnx = mysql.connector.connect(
                host='localhost',
                database='cars',
                user='root',
                password='root'
            )
            if __cnx.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            __cnx = None
    return __cnx
## get the all the products details:
connection=get_sql_connection()
cursor=connection.cursor()



# querry=("SELECT p.product_id,p.name,u.uom_name,p.price_per_unit FROM products p  INNER JOIN uom u ON p.uom_id=u.uom_id")
# cursor.execute(querry)
# response=[]
#
# for (product_id,name,uom_name,price_per_unit) in cursor:
#         response.append(
#             {'product_id':product_id, 'name':name, 'uom_name':uom_name, 'price_per_unit':price_per_unit}
#         )
#
# print(response)

# querry="SELECT p.name,u.uom_name,p.price_per_unit FROM products p INNER JOIN uom u ON p.uom_id=u.uom_id"
# cursor.execute(querry)
# records=[]
# for (product_name,uom_name,price_per_unit) in cursor:
#     records.append({"product_name":product_name,"uom_name":uom_name,"price_per_unit":price_per_unit})
#
# print(records)


# querry="SELECT id,model,brand,color,make FROM cars"
# cursor.execute(querry)
# rows=cursor.fetchone()
# for row in rows:
#     print(row)


# # Corrected SQL query
# query = "INSERT INTO cars (id, model, brand, color, make) VALUES (%s, %s, %s, %s, %s)"
#
# # Data to insert
# data = [
#     (1, 'Model S', 'Tesla', 'Red', 2021),
#     (10, 'Elantra', 'Hyundai', 'Grey', 2021),
#     (11, 'Creta', 'Hyundai', 'Black', 2022)
# ]
#
# # Executing the query for multiple records
# cursor.executemany(query, data)
# connection.commit()

# query="DELETE FROM cars WHERE model=%S"
# model=("Creta",)
# cursor.execute(query,model)
# print("model deleted suscssfully")
# # connection.commit()
# # SQL Query
# query = "DELETE FROM cars WHERE model=%s"
#
# # Data for the model
# model = ("Creta",)
#
# # Print the query and model for debugging
# print("Executing Query:", query)
# print("With Model:", model)
#
# # Execute the query
# cursor.execute(query, model)
# connection.commit()




query="DELETE FROM cars WHERE make=%s"
make = [(2021,), (2022,)]
cursor.executemany(query,make)
print("Exceuting querry :",query)
print("with makes:",make)
connection.commit()
print("querry comiited ")
# Adding a delay of 5 seconds before executing the query
print("Waiting for 60 seconds before executing the query...")
time.sleep(60)  # Delay for 5 second
connection.rollback()
print("querry rollbacked ")
